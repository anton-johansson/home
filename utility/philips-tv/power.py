from __future__ import print_function, unicode_literals
from datetime import datetime
import json
import sys
import requests
from requests.auth import HTTPDigestAuth
import argparse

# Turn off SSL warnings
requests.packages.urllib3.disable_warnings()

def power(host, username, password):
    print("Powering the TV on " + host + " on or off")
    response = requests.post("https://" + host + ":1926/6/input/key", json = {"key": "Standby"}, verify = False, auth = HTTPDigestAuth(username, password))
    if response.status_code != 200:
        print("Could not switch state")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description = "Powers the TV on or off.")
    parser.add_argument("--username", dest = "username", help = "Username")
    parser.add_argument("--password", dest = "password", help = "Password")
    parser.add_argument("host", help = "The host of the TV")
    args = parser.parse_args()
    host = args.host
    username = args.username
    password = args.password
    power(host, username, password)

main()
