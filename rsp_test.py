'''Module holding the main methods for performing response time testing.'''

import grequests
import requests
import csv
import datetime
import pymysql
###############################################################################

def main():
    today = datetime.date.today()
    with open('/root/ddos_detection/top-1m_{0}.csv'
         .format(today), 'r') as csvfile:
	
        raw = csv.reader(csvfile)
	alexa = [(rank, 'http://' + host) for rank, host in raw]
	alexa_chunks = []
	for x in range(0, len(alexa), 10):
   	    req = [grequests.head(u[1], timeout=1, allow_redirects=False) for u in alexa[x:x+10]]
            rsp = grequests.map(req)
	    durations = []
	    for a in rsp:
		try:
		    durations.append((a.url, a.elapsed))
		except:
		    pass
			
	    print durations
          
            




###############################################################################

if __name__ == '__main__':
    main()
