from __future__ import print_function, unicode_literals
from base64 import b64encode,b64decode
from datetime import datetime
import json
import sys
import requests
import random
import string
from Crypto.Hash import SHA, HMAC
from requests.auth import HTTPDigestAuth
import argparse

# Key used for generated the HMAC signature
secretKey = "ZmVay1EQVFOaZhwQ4Kv81ypLAZNczV9sG4KkseXWn1NEk6cXmPKO/MCa9sryslvLCFMnNe4Z4CPXzToowvhHvA=="

# Turn off SSL warnings
requests.packages.urllib3.disable_warnings()

def createDeviceId():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(16))

def createSignature(toSign):
    key = b64encode(secretKey.encode())
    signature = HMAC.new(key, toSign, SHA)
    return str(b64encode(signature.hexdigest().encode()))

def getDevice(deviceId):
    device = { "device_name": "AntonTV", "device_os": "Android", "app_name": "HomeAssistant", "type": "native" }
    device["app_id"] = "app.id"
    device["id"] = deviceId
    return device

def pair(host):
    print("Pairing Philips TV on host: " + host)

    # Generate new device
    deviceId = createDeviceId()
    device = getDevice(deviceId)

    # Build pairing request
    pairingRequest = { "scope": [ "read", "write", "control"] }
    pairingRequest["device"] = device

    # Perform pairing request
    print("Starting pairing request")
    pairingResponse = requests.post("https://" + host + ":1926/6/pair/request", json = pairingRequest, verify = False).json()
    if pairingResponse["error_id"] != "SUCCESS":
        print(pairingResponse["error_text"])
        exit(1)
    authenticationTimestamp = pairingResponse["timestamp"]
    authenticationKey = pairingResponse["auth_key"]

    # Ask for PIN code displayed on the TV
    pinCode = input("Enter PIN code displayed on the Philips TV: ")

    # Build grant request
    authentication = { "auth_AppId": "1" }
    authentication["pin"] = str(pinCode)
    authentication["auth_timestamp"] = authenticationTimestamp
    authentication["auth_signature"] = createSignature(str(authenticationTimestamp).encode() + str(pinCode).encode())
    grantRequest = {}
    grantRequest['auth'] = authentication
    grantRequest['device'] = device

    # Perform grant request
    print("Attempting to pair")
    grantResponse = requests.post("https://" + host + ":1926/6/pair/grant", json = grantRequest, verify = False, auth = HTTPDigestAuth(deviceId, authenticationKey)).json()
    if grantResponse["error_id"] != "SUCCESS":
        print(pairingResponse["error_text"])
        exit(1)

    # Output
    print("Username: " + deviceId)
    print("Password: " + authenticationKey)

def main():
    parser = argparse.ArgumentParser(description = 'Pairs a Philips TV.')
    parser.add_argument("host", help = "The host of the TV")
    args = parser.parse_args()
    host = args.host
    pair(host)

main()
