'''Module holding the main methods for performing response time testing.'''

import requests
import csv
import datetime
import pymysql
###############################################################################

def main():
    today = datetime.date.today()
    with open('/root/ddos_detection/top-1m_{date}.csv'
              .format(today), 'r') as csvfile:

        alexa = csv.reader(csvfile)
        for rank, host in alexa:
            rsp = requests.head('http://' + host)
	    print host, rsp.elapsed
            




###############################################################################

if __name__ == '__main__':
    main()
