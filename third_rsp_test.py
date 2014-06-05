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

queue_in = Queue.Queue()
results = {}
start = time.time()
ip_tried = []

class ThreadedHEAD(threading.Thread):
    """Threaded HEAD request"""
    def __init__(self, queue_in):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.queue_in = queue_in

    def run(self):
        while True:
            host = self.queue_in.get()
            try:
                print 'getting ip for', host
                ip = socket.gethostbyname(host)
                print 'ip for', host, 'is', ip
                if ip in ip_tried:
                    results[host] = 'already tried'
                    return
                else:
                    ip_tried.append(ip)
            except socket.gaierror:
                results[host] = 'no resolve'
                return
            try:
                print 'making request for', host
                r = requests.request("head", 'http://' + ip,
                    timeout=1, allow_redirects=False)
                time = r.elapsed.total_seconds()
            except requests.exceptions.Timeout:
                time = 'timeout'

            results[host] = time
            self.queue_in.task_done()

def main():
    alexa.update()
    today = datetime.date.today()
    with open('top-1m_{0}.csv'
         .format(today), 'r') as csvfile:
        raw = csv.reader(csvfile)
        alexa_list = [(rank, host) for rank, host in raw]

    for i in range(10):
        t = ThreadedHEAD(queue_in)
        t.start()

    for entry in alexa_list[20:29]:
        queue_in.put(entry[1])

    queue_in.join()

    print results
    print len(results)

###############################################################################

if __name__ == '__main__':
    main()
    print time.time() - start
