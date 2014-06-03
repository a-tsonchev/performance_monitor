'''Module holding the main methods for performing response time testing.'''

import csv
import datetime
import alexa
import Queue
import threading
import requests
import socket
import time

###############################################################################


queue = Queue.Queue()
results = {}
start = time.time()

class ThreadedHEAD(threading.Thread):
    """Threaded HEAD request"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            host = self.queue.get()
            try:
                ip = socket.gethostbyname(host)
            except socket.gaierror:
                results[host] = 'no resolve'
                return
            try:
                r = requests.request("head", 'http://' + ip, timeout=1, allow_redirects=False)
                time = r.elapsed.total_seconds()
            except requests.exceptions.Timeout:
                time = 'timeout'

            results[host] = time
            self.queue.task_done()

def main():
    alexa.update()
    today = datetime.date.today()
    with open('top-1m_{0}.csv'
         .format(today), 'r') as csvfile:    
        raw = csv.reader(csvfile)
        alexa = [(rank, host) for rank, host in raw]

    for i in range(50):
        t = ThreadedHEAD(queue)
        t.setDaemon(True)
        t.start()

    for entry in alexa[:50]:
        queue.put(entry[1])

    queue.join()

    print results
    print len(results)

###############################################################################

if __name__ == '__main__':
    main()
    print time.time() - start
    