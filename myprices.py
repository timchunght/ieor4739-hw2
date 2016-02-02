#!/usr/bin/python
import sys
import json
from pprint import pprint
import helpers


if len(sys.argv) != 2:  # the program name and the datafile
  # stop the program and print an error message
  sys.exit("usage: read1.py datafile ")

filename = sys.argv[1]

print "input", sys.argv[1]

helpers.download_json(filename, "data.json")