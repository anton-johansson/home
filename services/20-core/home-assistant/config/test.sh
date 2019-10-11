#!/bin/bash

cd "$(dirname "$0")"
HA_VERSION=$(cat ./.HA_VERSION)
docker run --rm -it --volume $(pwd):/config homeassistant/home-assistant:$HA_VERSION bash -c 'python3 -m homeassistant --config /config --script check_config'
