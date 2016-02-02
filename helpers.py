import json

def parse_json(data_filename, ticker_filename):
    try:
        data_file = open(data_filename, "r")
        data = json.load(data_file)
        ticker_file= open(ticker_filename, 'r')
       
    except IOError:
        print ("Cannot open file %s\n" % filename)
        sys.exit("bye")

    tickers = ticker_file.readlines();

    for ticker in tickers:
        ticker = ticker.split()[0]
        print data[ticker]
        print ticker

    data_file.close()
    ticker_file.close()

