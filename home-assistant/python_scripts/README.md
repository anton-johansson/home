# Python scripts

This directory contains various python scripts that can be executed by Home Assistant and that has access to Home Assistant services.


## twitch.py

Script for casting Twitch streams to the Chromecast. This is a workaround until (hopefully) Google Assistant gets native support for Twitch. The script contains a translation map that maps search phrases to specific Twitch streams. If none are matched, it'll attempt to load the stream with the exact search query.

This script is initated by IFTTT which in turns listens to Google Assistant instructions.
