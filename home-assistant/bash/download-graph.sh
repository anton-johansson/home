#!/bin/bash
#
## Downloads a graph from Grafana
##
## Parameters:
## - Grafana API key
## - Dashboard name
## - Panel ID
## - Output file name
##
## Example:
## ./download-graph.sh abc123 main 2 power-consumption.png

key=$1
dashboard=$2
panel=$3
file=$4

curl -s -H "Authorization: Bearer $key" "http://grafana:3000/render/d-solo/Uvy4M-mmk/$dashboard?orgId=1&panelId=$panel&width=800&height=400&tz=UTC%2B02%3A00" > /home/.homeassistant/downloads/$file
