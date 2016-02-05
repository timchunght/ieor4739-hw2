#!/usr/bin/python
import sys
import helpers
import stats
from pprint import pprint
import random


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

final_assets_rsquared_sums = {}
for i in range(100):
	original_rsquared_sum = helpers.selected_assets_rsquared_sum(selected_tickers, assets_dod_returns)
	final_assets_rsquared_sums[",".join(selected_tickers)] = float(original_rsquared_sum)
	bad_ticker = helpers.get_bad_ticker_in_selected_assets(original_rsquared_sum, selected_tickers, assets_dod_returns)
	available_tickers = list(set(assets_dod_returns.keys()) - set(selected_tickers))
	replacement_ticker = random.choice(available_tickers)
	selected_tickers.remove(bad_ticker)
	selected_tickers.append(replacement_ticker)

print "FINAL RESULT:"
print final_assets_rsquared_sums
print "MAX RSQUARED SUM:"
print max(final_assets_rsquared_sums.itervalues())
	# selected_tickers = new set of ticker with the bad ticker removed and replaced with a random one from the available_tickers

# print "RSQUARED: %f" % (original_rsquared_sum)
# remaining_assets 