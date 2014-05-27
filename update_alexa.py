'''Module to update the Alexa list of top million sites'''

import urllib
import os
import zipfile
import datetime

def main():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    if os.path.exists('top-1m_{0}.csv'.format(yesterday)):
        os.remove('top-1m_{0}.csv'.format(yesterday))
    if os.path.exists('top-1m_{0}.csv'.format(today)):
        os.remove('top-1m_{0}.csv'.format(today))

    urllib.urlretrieve('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip', 
		       'new_top-1m.csv.zip') 
    with zipfile.ZipFile('new_top-1m.csv.zip', 'r') as zip:
        zip.extractall('.')
        os.rename('top-1m.csv', 
                  'top-1m_{0}.csv'.format(today))        
    os.remove('new_top-1m.csv.zip')

if __name__ == '__main__':
    main()
