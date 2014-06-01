'''Module to update the Alexa list of top million sites'''

import urllib
import os
import zipfile
import datetime
import glob


def main():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)
    # old way of removing file without glob:
    # if os.path.exists('top-1m_{0}.csv'.format(yesterday)):
    #     os.remove('top-1m_{0}.csv'.format(yesterday))
    # if os.path.exists('top-1m_{0}.csv'.format(today)):
    #     os.remove('top-1m_{0}.csv'.format(today))
   
    urllib.urlretrieve('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip', 
		       'new_top-1m.csv.zip') 
    with zipfile.ZipFile('new_top-1m.csv.zip', 'r') as zip:
        zip.extractall('.')
        # check for existing today file
    if os.path.exists('top-1m_{0}.csv'.format(today)):
        os.remove('top-1m_{0}.csv'.format(today))
    os.rename('top-1m.csv', 
              'top-1m_{0}.csv'.format(today))        
    os.remove('new_top-1m.csv.zip')
    # remove any old files after the new one has been downloaded 
    file_list = glob.glob('top-1m_*.csv')
    for file in file_list:
        if file != 'top-1m_{0}.csv'.format(today):
            os.remove(file)

if __name__ == '__main__':
    main()
