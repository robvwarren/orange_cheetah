# Robert Warren - SID#: 28721802
# A module that is capable of downloading quotes from Yahoo Finance.

import http.client
import urllib.request
import urllib.error



def download_quotes(quote_url: str)->list:
    '''This function downloads quotes from the yahoo! finance server and
       returns a list containing the content from the url broken into lines.
    '''
    response = None
    try:
        print('Attempting to download the webpage...')
        response = urllib.request.urlopen(quote_url)
        print('Download successful.')
        contents = _parse_url_contents(response)
    except urllib.error.HTTPError as e:
        print('Something went wrong while downloading...')
        print('The returned status code is: {}'.format(e.code))
    finally:
        if response != None:
            response.close()        
    return(contents)


def _parse_url_contents(response: http.client.HTTPResponse) -> None:
    ''' Modeled from class example...
    '''
    content_bytes = response.read()
    content_string = content_bytes.decode(encoding='utf-8')
    content_lines = content_string.splitlines()
    
    return(content_lines[1:])
