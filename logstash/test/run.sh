#!/bin/bash

set -e
cd "$(dirname "$0")"

# Create a temporary folder
DIR=$(mktemp -d)
function finish {
  rm -rf "$DIR"
}
trap finish EXIT

# Combine all the test data into a single file
./combine_input.py "$DIR/input.json" test_cases/*.input.json

# Copy config, but replace input and output for mocks and asserts
mkdir "$DIR/pipeline"
cp ../pipeline/*.conf "$DIR/pipeline"
cp ./pipeline/*.conf "$DIR/pipeline"

# Run logstash
docker run --rm -it --user root --volume "$DIR":/test docker.elastic.co/logstash/logstash-oss:6.2.4 bash -c 'logstash -w 1 -f "/test/pipeline" <"/test/input.json"'

# Assert data
./compare.py "$DIR/output.json" test_cases/*.input.json
