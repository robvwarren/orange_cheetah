# Robert Warren - SID#: 28721802

import yahoo_quote
import datetime
import time
import indicators
import signals




def user_interface()->str:
    ''' This is the main entry point for the entire buying_stocks program.
        It takes no input and only interacts with the user through the console.
    '''
    print('*'*30)
    print("Rob Warren's Stock Buy/Sell Indicator Program")
    print("Version 1.0")
    print("Last Modified: 19 Feb 2014")
    print('*'*30)
    global SYMBOL
    global indicator_choice
    global indicator_N
    global indicator_string
    global buy_threshold
    global sell_threshold
    # we accept any ticker, but need to implement an exception if it fails later on
    SYMBOL = input("Enter a company's ticker symbol (e.g. 'BOO'): ")
    while True:
        start_date = input("Enter a start date for this analysis (of the form 'YYYY-MM-DD'): ")
        date_check = _start_date_check(start_date)
        if date_check:
            break
        else:
            print('That date is invalid.  Please enter a new date.')
    while True:
        end_date = input("Enter an end date for this analysis (of the form 'YYYY-MM-DD'): ")
        date_check = _end_date_check(end_date, start_date)
        if date_check:
            break
        else:
            print('That date is invalid.  Please enter a new date.')
    start_date = start_date.split('-')
    start_date[1] = _fix_month(start_date[1])
    end_date = end_date.split('-')
    end_date[1] = _fix_month(end_date[1])
    while True:
        indicator_choice = input('Select one of the following indicators...\nType "1" for a simple moving average indicator\nType "2" for a directional indicator\nYour Choice: ')
        indicator_check = _indicator_check(indicator_choice)
        if indicator_check:
            break
        else:
            print('That choice is invalid.  Please enter a new choice.')
    while True:
        indicator_N = input('Please enter the number of days to use for that indicator: ')
        try:
            indicator_N = int(indicator_N)
            if indicator_N > 0:
                break
            else:
                print('That choice is invalid.  Please enter a new choice.')
        except:
            print('That choice is invalid.  Please enter a new choice.')
    if indicator_choice == '2':
        while True:
            buy_threshold = input('Please enter the buy threshold: ')
            try:
                buy_threshold = int(buy_threshold)
                break
            except:
                print('That choice is invalid.  Please enter a new choice.')
        while True:
            sell_threshold = input('Please enter the sell threshold: ')
            try:
                sell_threshold = int(sell_threshold)
                break
            except:
                print('That choice is invalid.  Please enter a new choice.')
    else:
        buy_threshold = 'dummy'
        sell_threshold = 'dummy'
    indicator_string = _indicator_string(indicator_choice, indicator_N, buy_threshold, sell_threshold)
    quote_url = "http://ichart.yahoo.com/table.csv?s={}&a={}&b={}&c={}&d={}&e={}&f={}&g=d".format(
        SYMBOL, start_date[1], start_date[2], start_date[0], end_date[1], end_date[2], end_date[0]
        )
    return(quote_url)

def print_final_report(quote_array: list)->None:
    ''' This functions prints the "final report" to the console.
    '''
    global ticker
    global indicator_string
    global signal_string
    print("SYMBOL: ", SYMBOL)
    print("STRATEGY: {}".format(indicator_string))
    print()
    print('DATE        CLOSE       INDICATOR   SIGNAL')
    for line in quote_array:
        print('{:12}{:12}{:12}{:12}'.format(line[0], line[1], line[2], line[3]))

def _fix_month(month: str)->str:
    ''' A quick fix to convert months into a format acceptable by yahoo! finance.
        Takes a month of the format '01' as input and subtracts 1 from it... then returns
        a string of the same format '00'.
    '''
    if month == '12':
        month = '11'
    elif month == '11':
        month = '10'
    elif month == '10':
        month = '09'
    elif month == '09':
        month = '08'
    elif month == '08':
        month = '07'
    elif month == '07':
        month = '06'
    elif month == '06':
        month = '05'
    elif month == '05':
        month = '04'
    elif month == '04':
        month = '03'
    elif month == '03':
        month = '02'
    elif month == '02':
        month = '01'
    elif month == '01':
        month = '00'
    return month

def _establish_quote_array(all_data: list)-> list:
    ''' Takes the full dataset from the url as input (list) and outputs a new array
        that will be used to generate buy sell signals (list).
    '''
    parsed_data = []
    result = []
    for line in all_data:
        parsed_data.append(line.split(','))
    for line in parsed_data:
        result.append([line[0], line[4], '', ''])
    result.reverse()
    return(result)

def _start_date_check(date: str)->bool:
    ''' This function checks to make sure the user entered a valid start date
        for this stock quote analysis program.
    '''
    now = datetime.datetime.now()
    now = datetime.datetime.strftime(now, '%Y-%m-%d')
    now = time.strptime(now, '%Y-%m-%d')
    try:
        if len(date) != 10:
            result = False
            return(result)
        date = time.strptime(date, '%Y-%m-%d')
        result = True
        date = time.mktime(date)
        now = time.mktime(now)
        if date > now:
            result = False
            return(result)
        else:
            return(result)
    except:
        result = False
        return(result)

def _end_date_check(end_date: str, start_date: str)->bool:
    ''' This function checks to make sure the user entered a valid end date
        for this stock quote analysis program.
    '''
    now = datetime.datetime.now()
    now = datetime.datetime.strftime(now, '%Y-%m-%d')
    now = time.strptime(now, '%Y-%m-%d')
    try:
        if len(end_date) != 10:
            result = False
            return(result)
        end_date = time.strptime(end_date, '%Y-%m-%d')
        start_date = time.strptime(start_date, '%Y-%m-%d')
        result = True
        end_date = time.mktime(end_date)
        start_date = time.mktime(start_date)
        now = time.mktime(now)
        if (start_date < end_date) and (end_date < now):
            return(result)
        else:
            result = False
            return(result)
    except:
        result = False
        return(result)

def _indicator_check(choice: str)->bool:
    ''' This function quickly checks if the user entered an indicator choice correctly.
    '''
    if choice == '1':
        return(True)
    elif choice == '2':
        return(True)
    else:
        return(False)

def _indicator_string(choice: str, length: int, buy_threshold: int, sell_threshold: int)->str:
    ''' This function handles the user's choice of indicator (either a "1" or a "2")
        and returns a string with a more complete description of the choice.
    '''
    if choice == '1':
        return('Simple moving average ({}-day)'.format(str(length)))
    elif choice == '2':
        if (buy_threshold > 0) and (sell_threshold > 0):
            return('Directional ({}-day), buy above +{}, sell below +{}'.format(str(length), str(buy_threshold), str(sell_threshold)))
        elif (buy_threshold > 0) and (sell_threshold <= 0):
            return('Directional ({}-day), buy above +{}, sell below {}'.format(str(length), str(buy_threshold), str(sell_threshold)))
        elif (buy_threshold <= 0) and (sell_threshold > 0):
            return('Directional ({}-day), buy above {}, sell below +{}'.format(str(length), str(buy_threshold), str(sell_threshold)))
        elif (buy_threshold <= 0) and (sell_threshold <= 0):
            return('Directional ({}-day), buy above {}, sell below {}'.format(str(length), str(buy_threshold), str(sell_threshold)))

if __name__ == '__main__':
    try:
        quote_url = user_interface()
        data = yahoo_quote.download_quotes(quote_url)
        quote_array = _establish_quote_array(data)
        if indicator_choice == '1':
            result = indicators.SimpleMovingAverage(quote_array, indicator_N)
        elif indicator_choice == '2':
            result = indicators.Directional(quote_array, indicator_N)
        result = result.execute()
        if indicator_choice == '1':
            result = signals.SimpleMovingAverage(result, indicator_N)
        elif indicator_choice == '2':
            result = signals.Directional(result, buy_threshold, sell_threshold)
        result = result.execute()
        print_final_report(result)
    except:
        print('Seems like something bad happened.  Something very bad.')
    finally:
        print("Thanks for running the program!  Please run again if you want to know something else!")
