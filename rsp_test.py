'''Module holding the main methods for performing response time testing.'''

import requests
import csv
import datetime
###############################################################################

def main():
    with open('/root/ddos_detection/top-1m_{date}.csv'
              .format(date=datetime.date.today()), 'r') as csvfile:

        alexa = csv.reader(csvfile)
        for rank, host in alexa:
            rsp = requests.head('http://' + host)
	    print host, rsp.elapsed
            




###############################################################################

if __name__ == '__main__':
    main()
