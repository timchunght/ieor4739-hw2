import json
import sys
from yahoo_finance import Share
import stats
import numpy as np



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
    all_asset_tickers = assets_dod_returns.keys()
    selected_assets = []
    for ticker in selected_tickers:
        selected_assets.append(assets_dod_returns[ticker])

    rsquared_sum = 0
    for ticker in all_asset_tickers:
        rsquared_sum += stats.reg0_m(assets_dod_returns[ticker], selected_assets).rsquared
    return rsquared_sum

def calculate_V(selected_tickers, assets_dod_returns, save_file=False):

    # this is the difference between all the assets tickers and the selected asset tickers
    # this is all the possible y's
    print "calculate V for %s" % (",".join(selected_tickers))
    all_asset_tickers = assets_dod_returns.keys()
    selected_assets = []
    for ticker in selected_tickers:
        selected_assets.append(assets_dod_returns[ticker])

    V = np.ndarray(shape=(len(selected_tickers), len(all_asset_tickers)))
    # use regression to get coefficients for all assets
    for i in xrange(len(all_asset_tickers)):
        ticker = all_asset_tickers[i] 
        # selected_assets is 10 x T
        results = stats.reg0_m(assets_dod_returns[ticker], selected_assets)
        V[:, i] = results.params
 
    print "Size of V: "
    # V is a 10 x N matrix
    print V.shape
    # F is 10 x 10
    F = np.cov(selected_assets)
    print "Size of F: "
    print F.shape
    # Q is a N (total number of assets) x N (Q is covariance matrix)
    Q = np.cov(assets_dod_returns.values())
    print "Size of Q: "
    print Q.shape
    # VTransFV is N x N matrix;  
    VTransFV = np.dot(np.dot(np.transpose(V), F), V)
    print "Size of V^T *F*V: "
    print VTransFV.shape
    # R is a (Residual Matrix) (N x N)
    R = Q - VTransFV
    print "Size of R: "
    print R.shape
    # "sigma squared" coefficients, variances (sigma^2) are the diagonal of a covariances 
    # but we only need the residual in this case
    # only keep the diagonal
    DiagR = np.diag(R) 
    print "Size of Diagonal R: "
    print DiagR.shape

    if save_file:
        np.savetxt("-".join(selected_tickers) + "-V", V)
        np.savetxt("-".join(selected_tickers) + "-F", F)
        np.savetxt("-".join(selected_tickers) + "-Q", Q)
        np.savetxt("-".join(selected_tickers) + "-VTransFV", VTransFV)
        np.savetxt("-".join(selected_tickers) + "-R", R)
        np.savetxt("-".join(selected_tickers) + "-DiagonalR", DiagR)
        
    return


 
