# -*- coding: utf-8 -*-
from datetime import timedelta
from tornado import httpclient, gen, ioloop, queues

concurrency = 10


@gen.coroutine
def get_links_from_url(url):
    try:
        response = yield httpclient.AsyncHTTPClient().fetch(url)
    except Exception as e:
        print('Exception: %s %s' % (e, url))
        raise gen.Return(None)
    raise gen.Return(response)


@gen.coroutine
def main():
    q = queues.Queue()

    @gen.coroutine
    def fetch_url():
        current_url = yield q.get()
        print current_url
        try:
            response = yield get_links_from_url(current_url)
            if response:
                # print response.body
                print response
            else:
                print response
        except Exception, e:
            print str(e)
        finally:
            print 'task_done'
            q.task_done()

    @gen.coroutine
    def worker():
        while True:
            yield fetch_url()

    q.put('http://www.google.com.hk/webhp?hl=zh-CN&sourceid=cnhp')
    q.put('http://www.baidu.com/')
    q.put('http://www.163.com/')

    # Start workers, then wait for the work queue to be empty.
    for _ in range(concurrency):
        worker()
    yield q.join(timeout=timedelta(seconds=300))

    q.put('http://www.baidu.com/')
    for _ in range(concurrency):
        worker()
    yield q.join(timeout=timedelta(seconds=300))

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)
