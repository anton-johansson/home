"""Philips TV"""
import homeassistant.helpers.config_validation as cv
import argparse
import json
import random
import requests
import urllib3
import string
import sys
import voluptuous as vol

from base64 import b64encode,b64decode
from Crypto.Hash import SHA, HMAC
from datetime import timedelta, datetime
from homeassistant.components.media_player import (SUPPORT_STOP, SUPPORT_PLAY, SUPPORT_NEXT_TRACK, SUPPORT_PAUSE,
                                                   SUPPORT_PREVIOUS_TRACK, SUPPORT_VOLUME_SET, PLATFORM_SCHEMA, SUPPORT_TURN_OFF, SUPPORT_TURN_ON,
                                                   SUPPORT_VOLUME_MUTE, SUPPORT_VOLUME_STEP, MediaPlayerDevice)
from homeassistant.const import (CONF_HOST, CONF_NAME, CONF_USERNAME, CONF_PASSWORD,
                                 STATE_OFF, STATE_ON, STATE_UNKNOWN)
from homeassistant.util import Throttle
from requests.auth import HTTPDigestAuth
from requests.adapters import HTTPAdapter

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=5)

SUPPORT_PHILIPS_2016 = SUPPORT_STOP | SUPPORT_TURN_OFF | SUPPORT_TURN_ON | SUPPORT_VOLUME_STEP | \
                       SUPPORT_VOLUME_MUTE | SUPPORT_VOLUME_SET |SUPPORT_NEXT_TRACK | \
                       SUPPORT_PAUSE | SUPPORT_PREVIOUS_TRACK | SUPPORT_PLAY

DEFAULT_DEVICE = 'default'
DEFAULT_HOST = '127.0.0.1'
DEFAULT_USER = 'user'
DEFAULT_PASS = 'pass'
DEFAULT_NAME = 'Philips TV'
BASE_URL = 'https://{0}:1926/6/{1}'
TIMEOUT = 5.0
CONNFAILCOUNT = 5

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST, default=DEFAULT_HOST): cv.string,
    vol.Required(CONF_USERNAME, default=DEFAULT_USER): cv.string,
    vol.Required(CONF_PASSWORD, default=DEFAULT_PASS): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
})

# Disable SSL warnings. I assume this is globally, is there a way to do this for the created session only?
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Philips 2016+ TV platform."""
    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    user = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    tvapi = PhilipsTVBase(host, user, password)
    add_devices([PhilipsTV(tvapi, name)])

class PhilipsTV(MediaPlayerDevice):
    """Representation of a 2016+ Philips TV exposing the JointSpace API."""

    def __init__(self, tv, name):
        """Initialize the TV."""
        self._tv = tv
        self._default_name = name
        self._name = name
        self._StateC = None
        self._state = STATE_UNKNOWN
        self._min_volume = 0
        self._max_volume = 60
        self._volume = 0
        self._muted = False
        self._channel_id = None
        self._channel_name = None
        self._connfail = 0

    @property
    def name(self):
        """Return the device name."""
        return self._name

    @property
    def StateC(self):
        """Return the device name."""
        return self._StateC

    @property
    def should_poll(self):
        """Device should be polled."""
        return True

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        return SUPPORT_PHILIPS_2016

    @property
    def state(self):
        """Get the device state. An exception means OFF state."""
        return self._state

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._volume / self._max_volume

    @property
    def is_volume_muted(self):
        """Boolean if volume is currently muted."""
        return self._muted

    def turn_off(self):
        """Turn off the device."""
        self._tv.sendKey('Standby')
        self._state = STATE_OFF

    def turn_on(self):
        """Turn on the device."""
        self._tv.sendKey('Standby')
        self._state = STATE_ON

    def volume_up(self):
        """Send volume up command."""
        self._tv.sendKey('VolumeUp')

    def volume_down(self):
        """Send volume down command."""
        self._tv.sendKey('VolumeDown')

    def set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        tv_volume = volume * self._max_volume
        self._tv.setVolume(tv_volume)

    def mute_volume(self, mute):
        """Send mute command."""
        self._tv.sendKey('Mute')

    def media_play(self):
        """Send media play command to media player."""
        self._tv.sendKey('Play')

    def media_play_pause(self):
        self._tv.sendKey('PlayPause')

    def media_pause(self):
        """Send media pause command to media player."""
        self._tv.sendKey('Pause')

    def media_stop(self):
        """Send media stop command to media player."""
        self._tv.sendKey('Stop')

    def media_next_track(self):
        """Send next track command."""
        self._tv.sendKey('FastForward')

    def media_previous_track(self):
        """Send the previous track command."""
        self._tv.sendKey('Rewind')

    @property
    def media_title(self):
        """Title of current playing media."""
        return self._channel_name

    @property
    def media_content_id(self):
        return self._channel_id

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data and update device state."""
        self._tv.update()
        self._min_volume = self._tv.min_volume
        self._max_volume = self._tv.max_volume
        self._channel_id = self._tv.channel_id
        self._channel_name = self._tv.channel_name
        self._volume = self._tv.volume
        self._muted = self._tv.muted
        self._StateC = self._tv.StateC
        self._name = self._default_name
        if self._StateC == 'On':
            self._state = STATE_ON
        elif self._StateC == 'Standby':
            self._state = STATE_OFF
        else:
            self._state = STATE_UNKNOWN

class PhilipsTVBase(object):
    def __init__(self, host, user, password):
        self._host = host
        self._user = user
        self._password = password
        self._connfail = 0
        self.on = None
        self.name = None
        self.min_volume = None
        self.max_volume = None
        self.volume = None
        self.muted = None
        self.sources = None
        self.source_id = None
        self.channels = None
        self.channel_id = None
        self.channel_name = None
        self.StateC = None

        # The XTV app appears to have a bug that limits the nummber of SSL sessions to 100
        # The code below forces the control to keep re-using a single connection
        self._session = requests.Session()
        self._session.mount('https://', HTTPAdapter(pool_connections=1))

    def _getReq(self, path):
        try:
            if self._connfail:
                self._connfail -= 1
                return None
            resp = self._session.get(BASE_URL.format(self._host, path), verify=False, auth=HTTPDigestAuth(self._user, self._password), timeout=TIMEOUT)
            self.on = True
            return json.loads(resp.text)
        except requests.exceptions.RequestException as err:
            self._connfail = CONNFAILCOUNT
            self.on = False
            return None

    def _postReq(self, path, data):
        try:
            if self._connfail:
                self._connfail -= 1
                return False
            resp = self._session.post(BASE_URL.format(self._host, path), data=json.dumps(data), verify=False, auth=HTTPDigestAuth(self._user, self._password), timeout=TIMEOUT)
            self.on = True
            if resp.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as err:
            self._connfail = CONNFAILCOUNT
            self.on = False
            return False

    def update(self):
        self.getName()
        self.getAudiodata()
        self.getChannel()
        self.getStateC()

    def getChannel(self):
        r = self._getReq('activities/tv')
        if r:
            self.channel_id = r["channel"]["preset"]
            self.channel_name = r["channel"]["name"]

    def getName(self):
        r = self._getReq('system/name')
        if r:
            self.name = r['name']


    def getStateC(self):
        r = self._getReq('powerstate')
        if r:
            self.StateC = r['powerstate']

    def getAudiodata(self):
        audiodata = self._getReq('audio/volume')
        if audiodata:
            self.min_volume = int(audiodata['min'])
            self.max_volume = int(audiodata['max'])
            self.volume = audiodata['current']
            self.muted = audiodata['muted']
        else:
            self.min_volume = None
            self.max_volume = None
            self.volume = None
            self.muted = None

    def setVolume(self, level):
        if level:
            if self.min_volume != 0 or not self.max_volume:
                self.getAudiodata()
            if not self.on:
                return
            try:
                targetlevel = int(level)
            except ValueError:
                return
            if targetlevel < self.min_volume + 1 or targetlevel > self.max_volume:
                return
            self._postReq('audio/volume', {'current': targetlevel, 'muted': False})
            self.volume = targetlevel

    def sendKey(self, key):
        self._postReq('input/key', {'key': key})
