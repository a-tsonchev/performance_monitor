'''Module holding the main methods for performing response time testing.'''

from requests_futures.sessions import FuturesSession
import csv
import datetime
import pymysql
###############################################################################

def main():
    today = datetime.date.today()
    with open('top-1m_{0}.csv'
         .format(today), 'r') as csvfile:
	
        raw = csv.reader(csvfile)
	alexa = [(rank, 'http://' + host) for rank, host in raw]
	session = FuturesSession(max_workers=200)
	reqs = []
	for entry in alexa[:200]:
		url = entry[1]
		reqs.append((url, session.head(url)))
	print reqs
	for req in reqs:
		print req[0], req[1].result().elapsed


###############################################################################

if __name__ == '__main__':
    main()
