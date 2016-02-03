#!/usr/bin/python
import sys
import helpers
import stats
from pprint import pprint


if len(sys.argv) != 2:  # the program name and the datafile
  # stop the program and print an error message
  sys.exit("usage: ./json_parser datafile")

data_filename = sys.argv[1]
print "data input: ", sys.argv[1]
prices = helpers.parse_json(data_filename)

assets_dod_returns = helpers.multi_asset_day_over_day_returns(prices)

print "ZNGA DOD"
print assets_dod_returns["ZNGA"]
print len(assets_dod_returns["ZNGA"])
# print assets_dod_returns.keys()