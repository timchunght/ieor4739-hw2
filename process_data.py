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
# in this hash, the key will be the ticker removed
new_rsquared_sums = {}
for i in range(len(selected_tickers)):
	new_selected_tickers = list(selected_tickers)
	ticker = new_selected_tickers[i]
	del(new_selected_tickers[i])
	new_rsquared_sums[ticker] = helpers.selected_assets_rsquared_sum(new_selected_tickers, assets_dod_returns)
new_rsquared_sums_diff = {}
for key in new_rsquared_sums.keys():
	new_rsquared_sums_diff[key] = original_rsquared_sum - new_rsquared_sums[key]
min_val = min(new_rsquared_sums_diff.itervalues())
bad_ticker = [k for k, v in new_rsquared_sums_diff.iteritems() if v == min_val][0]

bad_ticker



# print "RSQUARED: %f" % (original_rsquared_sum)
# remaining_assets 