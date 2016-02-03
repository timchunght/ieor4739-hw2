#!/usr/bin/python
import sys
import json
from pprint import pprint
import helpers


if len(sys.argv) != 3:  # the program name and the datafile
  # stop the program and print an error message
  sys.exit("usage: read1.py data_file output_name.json")

filename = sys.argv[1]
output_filename = sys.argv[2]
print "Input: ", sys.argv[1]
print "Output: ", sys.argv[2]

helpers.download_json(filename, output_filename)