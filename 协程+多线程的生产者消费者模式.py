# -*- coding: utf-8 -*-
import multiprocessing


def producer():
    print 'receive'
    while 1:
        n = yield
        print str(n)

 
def consumer(msg):
    m = producer()
    m.next()
    for i in xrange(3):
        m.send(msg)
 
if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=6)
    for i in xrange(5):
        msg = str(i)
        pool.apply_async(consumer, (msg, ))
    pool.close()
    pool.join()
