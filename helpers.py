import json
import sys
from yahoo_finance import Share
def parse_json(data_filename, ticker_filename):
    try:
        data_file = open(data_filename, "r")
        data = json.load(data_file)
        ticker_file= open(ticker_filename, 'r')
       
    except IOError:
        print ("Cannot open file %s\n" % filename)
        sys.exit("bye")

    prices = {}
    tickers = ticker_file.readlines();
    for ticker in tickers:
        ticker = ticker.split()[0]
        if ticker in data.keys():
            print ticker
            stock_data = data[ticker]
            prices[ticker] = [0 for j in xrange(len(stock_data))]
            for j in xrange(len(stock_data)):
                # print str(j) + " price: " + stock_data[j]['Adj_Close']
                prices[ticker][j] = stock_data[j]['Adj_Close']
            print prices[ticker]
    data_file.close()
    ticker_file.close()
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
