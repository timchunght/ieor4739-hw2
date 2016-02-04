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

original_rsquared_sum = helpers.selected_assets_rsquared_sum(selected_tickers, assets_dod_returns)
print helpers.get_bad_ticker_in_selected_assets(original_rsquared_sum, selected_tickers, assets_dod_returns)

# print "RSQUARED: %f" % (original_rsquared_sum)
# remaining_assets 