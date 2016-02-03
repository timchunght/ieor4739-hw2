#!/usr/bin/python
import sys
import helpers
from pprint import pprint


if len(sys.argv) != 3:  # the program name and the datafile
  # stop the program and print an error message
  sys.exit("usage: json_parser.py datafile ")

data_filename = sys.argv[1]
ticker_filename = sys.argv[2]
print "data input", sys.argv[1]
print "ticker input", sys.argv[2]
prices = helpers.parse_json(data_filename, ticker_filename)

print helpers.multi_asset_day_over_day_returns(prices)