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

# this block of code removes data of irregular length
for key in assets_dod_returns.keys():
	if len(assets_dod_returns[key]) != 503:
		del(assets_dod_returns[key])


selected_tickers = ["FOXA", "FOX", "DDD", "MMM", "AAN", "ABT", "ABBV", "ACHC", "ACN", "ACE"]
# this is the difference between all the assets tickers and the selected asset tickers
# this is all the possible y's
remaining_tickers = list(set(assets_dod_returns.keys()) - set(selected_tickers))
selected_assets = []
for ticker in selected_tickers:
	selected_assets.append(assets_dod_returns[ticker])

rsquared_sum = 0
for ticker in remaining_tickers:
	rsquared_sum += stats.reg0_m(assets_dod_returns[ticker], selected_assets).rsquared

print "RSQUARED: %f" % (rsquared_sum)
# remaining_assets 