'''Module to update the Alexa list of top million sites'''

import urllib
import os
import zipfile
import datetime

def main():
    urllib.urlretrieve('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip', 
		        '/root/ddos_detection/new_top-1m.csv.zip') 
    with zipfile.ZipFile('/root/ddos_detection/new_top-1m.csv.zip', 'r') as zip:
        zip.extractall('/root/ddos_detection')
        os.rename('/root/ddos_detection/top-1m.csv', 
                  '/root/ddos_detection/top-1m_{date}.csv'.format(
                  date=datetime.date.today()))        
    os.remove('/root/ddos_detection/new_top-1m.csv.zip')

if __name__ == '__main__':
    main()
