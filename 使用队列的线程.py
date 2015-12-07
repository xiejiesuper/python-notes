import threading
from Queue import Queue 

class WorkerThread(threading.Thread):
    def __init__(self,*args,**kwargs):
        threading.Thread.__init__(self,*args,**kwargs)
        self.input_queue = Queue()
    def send(self,item):
        self.input_queue.put(item)
    def close(self):
        self.input_queue.put(None)
        self.input_queue.join()
    def run(self):
        while True:
            item = self.input_queue.get()
            if item is None:
                print 'break'
                break
            print item
            self.input_queue.task_done()

w = WorkerThread()
w.start()
w.send("hello")
w.send("word")
w.close()
