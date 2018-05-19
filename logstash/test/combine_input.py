#!/usr/bin/env python3

import sys

COMBINED_NAME = sys.argv[1]
IN_NAMES = sys.argv[2:]

with open(COMBINED_NAME, "w") as f:
    for i in IN_NAMES:
        f.write(open(i).read().replace("\n", "") + "\n")
