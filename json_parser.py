#!/usr/bin/python
import sys
import json
from yahoo_finance import Share
from pprint import pprint


if len(sys.argv) != 2:  # the program name and the datafile
  # stop the program and print an error message
  sys.exit("usage: json_parser.py datafile ")

filename = sys.argv[1]

print "data input", sys.argv[1]

try:
    datafile = open(filename, "r")
    data = json.load(datafile)
    print data
    datafile.close()
except IOError:
    print ("Cannot open file %s\n" % filename)
    sys.exit("bye")



