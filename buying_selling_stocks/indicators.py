# Robert Warren - SID#: 28721802

#A module that implements the two indicators. These must be implemented as classes.

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
        for i in range(self._N,len(self._quotes)+1):
            temp_quotes = []
            for row in self._quotes[i-self._N:i]:
                temp_quotes.append(eval(row[1]))
            temp_sum = sum(temp_quotes)
            indicator = temp_sum/self._N
            self._quotes[i-1][2] = "{0:.2f}".format(indicator)
        return(self._quotes)


class Directional:
    def __init__(self, quotes: list, indicator_N: int):
        ''' Initializes the Directional indicator set to work
            with a given list of quotes.
        '''
        self._quotes = quotes
        self._N = indicator_N
          

    def execute(self) -> list:
        ''' Calculates and returns a new array that includes the quotes
            and the list of indicators.
        '''
        for i in range(0,len(self._quotes)):
            temp_quotes = []
            if i <= self._N:
                for row in self._quotes[0:i+1]:
                    temp_quotes.append(eval(row[1]))
                indicator = 0
                if len(temp_quotes) == 1:
                    pass
                else:
                    for x in range(1, len(temp_quotes)):
                        if temp_quotes[x] > temp_quotes[x-1]:
                            indicator += 1
                        elif temp_quotes[x] < temp_quotes[x-1]:
                            indicator -= 1
                        else:
                            pass
            else:
                for row in self._quotes[i-self._N:i+1]:
                    temp_quotes.append(eval(row[1]))
                indicator = 0
                for x in range(1, len(temp_quotes)):
                    if temp_quotes[x] > temp_quotes[x-1]:
                        indicator += 1
                    elif temp_quotes[x] < temp_quotes[x-1]:
                        indicator -= 1
                    else:
                        pass
            if indicator > 0:
                self._quotes[i][2] = "+{}".format(indicator)
            else:
                self._quotes[i][2] = "{}".format(indicator)
        return(self._quotes)
