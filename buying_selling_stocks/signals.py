# Robert Warren - SID#: 28721802

# A module that implements the signal strategies. These must be implemented as classes.

class SimpleMovingAverage:
    def __init__(self, quotes: list, indicator_N: int):
        ''' Initializes the SimpleMovingAverage indicator set to work
            with a given list of quotes.
        '''
        self._quotes = quotes
        self._N = indicator_N
            

    def execute(self) -> list:
        ''' Calculates and returns a new array that includes the quotes
            and the list of indicators.
        '''
        for i in range(self._N,len(self._quotes)):
            today = self._quotes[i][1]
            yesterday = self._quotes[i-1][1]
            today_avg = self._quotes[i][2]
            yesterday_avg = self._quotes[i-1][2]
            if (today > today_avg) and (yesterday <= yesterday_avg):
                self._quotes[i][3] = 'BUY'
            elif (today < today_avg) and (yesterday >= yesterday_avg):
                self._quotes[i][3] = 'SELL'
            else:
                pass
        return(self._quotes)


class Directional:
    def __init__(self, quotes: list, buy_threshold: int, sell_threshold: int):
        ''' Initializes the Directional indicator set to work
            with a given list of quotes.
        '''
        self._quotes = quotes
        self._buy = buy_threshold
        self._sell = sell_threshold

    def execute(self) -> list:
        ''' Calculates and returns a new array that includes the quotes
            and the list of indicators.
        '''
        for i in range(1,len(self._quotes)):
            today = eval(self._quotes[i][2].strip('+'))
            yesterday = eval(self._quotes[i-1][2].strip('+'))
            if (today > self._buy) and (yesterday <= self._buy):
                self._quotes[i][3] = 'BUY'
            elif (today < self._sell) and (yesterday >= self._sell):
                self._quotes[i][3] = 'SELL'
            else:
                pass
        return(self._quotes)
