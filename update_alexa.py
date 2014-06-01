'''Module to update the Alexa list of top million sites'''

import urllib
import os
import zipfile
import datetime
import glob
import requests
import StringIO


def main():
    today = datetime.date.today()
    today_csv = 'top-1m_{0}.csv'.format(today)
    response = requests.get('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip')
    data = response.content
    zip = zipfile.ZipFile(StringIO.StringIO(data), 'r')
    with open(today_csv, 'w') as outfile:
        outfile.write(zip.read('top-1m.csv'))
    # remove any old files after the new one has been downloaded 
    file_list = glob.glob('top-1m_*.csv')
    for file in file_list:
        if file != today_csv:
            os.remove(file)

if __name__ == '__main__':
    main()
