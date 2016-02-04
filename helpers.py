import json
import sys
from yahoo_finance import Share
import stats

def parse_json(data_filename):
    try:
        data_file = open(data_filename, "r")
        data = json.load(data_file)
    except IOError:
        print ("Cannot open file %s\n" % data_filename)
        sys.exit("bye")

    prices = {}
    for ticker in data.keys():
        # print ticker
        stock_data = data[ticker]
        prices[ticker] = [0 for j in xrange(len(stock_data))]
        for j in xrange(len(stock_data)):
            # print str(j) + " price: " + stock_data[j]['Adj_Close']
            prices[ticker][j] = float(stock_data[j]['Adj_Close'])
        prices[ticker].reverse()
        # print prices[ticker]
    data_file.close()
    return prices

def download_json(ticker_filename, output_filename):
    try:
        ticker_file = open(ticker_filename, 'r') # opens the input file
        output_file = open(output_filename, "w")
    except IOError:
        print ("Cannot open file %s\n" % ticker_filename)
        sys.exit("bye")

    lines = ticker_file.readlines();

    count = 1
    prices = {}
    for line in lines:
        thisline = line.split()
        if len(line) > 0:
            ticker = thisline[0]
            try:
                
                print (str(count) + " " + ticker)

                share = Share(ticker)
                everything = share.get_historical('2014-01-01', '2015-12-31')
                # prices[thisline[0]] = [0 for j in xrange(len(everything))]
        #         for j in xrange(len(everything)):
        # #            print str(j) + " price: " + everything[j]['Adj_Close']
        #             prices[thisline[0]][j] = everything[j]['Adj_Close']
                
                prices[ticker] = everything
                print ticker
                count += 1
            except:
                print "cannot retrieve data for ticker: %s" % (ticker)

    json.dump(prices, output_file)          

    ticker_file.close()
    output_file.close()

# return an array of day over day return for a single asset
def one_asset_day_over_day_returns(prices_arr):
    length = len(prices_arr)
    day_over_day_returns = []
    total = float(0)
    for idx, current_price in enumerate(prices_arr):
        if idx < length - 1:
            daily_return = (prices_arr[idx+1] - current_price)/current_price
            total += daily_return
            day_over_day_returns.append(daily_return)

    mean = total/(length - 1)
    day_over_day_returns[:] = [value - mean for value in day_over_day_returns]
    # print day_over_day_returns
    # print len(prices_arr)
    # print len(day_over_day_returns)
    return day_over_day_returns

# return a hash/dict of day of day returns for multiple assets; 
# the key is the ticker and the value is its day of day returns
def multi_asset_day_over_day_returns(prices):
    returns = {}
    for ticker in prices.keys():
        if len(prices[ticker]) != 0:
            returns[ticker] = one_asset_day_over_day_returns(prices[ticker])
    # print returns 
    return returns
    

def selected_assets_rsquared_sum(selected_tickers, assets_dod_returns):
    # this is the difference between all the assets tickers and the selected asset tickers
    # this is all the possible y's
    print "Calculating r-squared for the following assets: %s" % (",".join(selected_tickers))
    remaining_tickers = list(set(assets_dod_returns.keys()) - set(selected_tickers))
    selected_assets = []
    for ticker in selected_tickers:
        selected_assets.append(assets_dod_returns[ticker])

    rsquared_sum = 0
    for ticker in remaining_tickers:
        rsquared_sum += stats.reg0_m(assets_dod_returns[ticker], selected_assets).rsquared
    return rsquared_sum

def get_bad_ticker_in_selected_assets(selected_tickers, assets_dod_returns):
    original_rsquared_sum = selected_assets_rsquared_sum(selected_tickers, assets_dod_returns)
    # in this hash, the key will be the ticker removed
    new_rsquared_sums = {}
    for i in range(len(selected_tickers)):
        new_selected_tickers = list(selected_tickers)
        ticker = new_selected_tickers[i]
        del(new_selected_tickers[i])
        new_rsquared_sums[ticker] = selected_assets_rsquared_sum(new_selected_tickers, assets_dod_returns)
    new_rsquared_sums_diff = {}
    for key in new_rsquared_sums.keys():
        new_rsquared_sums_diff[key] = original_rsquared_sum - new_rsquared_sums[key]
    min_val = min(new_rsquared_sums_diff.itervalues())
    return [k for k, v in new_rsquared_sums_diff.iteritems() if v == min_val][0]