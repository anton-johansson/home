#!/usr/bin/env python3

import json
import os
import sys

from difflib import unified_diff

PROCESSED_NAME = sys.argv[1]
IN_NAMES = sys.argv[2:]


def format(content):
    try:
        obj = json.loads(content)
    except ValueError as e:
        raise SystemExit(e)

    return json.dumps(obj, sort_keys=True,
                      indent=4, separators=(',', ': ')) + "\n"


def to_lines(content):
    return [x + "\n" for x in content.split("\n")]


processed_lines = open(PROCESSED_NAME).readlines()

assert len(processed_lines) == len(IN_NAMES)

ok = 0
failed = 0
for index, processed_line in enumerate(processed_lines):
    assert IN_NAMES[index].endswith(".input.json")
    stem = IN_NAMES[index].replace(".input.json", "")
    expected_name = stem + ".expected-output.json"
    actual = to_lines(format(processed_line))
    with open(stem + ".output.json", "w") as f:
        f.writelines(actual)
    if not os.path.isfile(expected_name):
        print (stem + ": FAIL, missing file " + expected_name)
        failed += 1
    else:
        expected = open(expected_name).read()
        expected = to_lines(format(expected))
        if actual == expected:
            print (stem + ": OK")
            ok += 1
        else:
            print (stem + ": FAIL")
            failed += 1
            for line in unified_diff(expected, actual, fromfile='expected.json', tofile='actual.json'):
                sys.stdout.write(line)

if failed > 0 or ok == 0:
    sys.exit(1)
else:
    sys.exit(0)
