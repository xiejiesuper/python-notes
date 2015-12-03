# coding:utf-8
import signal
import time
import contextlib


@contextlib.contextmanager
def execution_timeout(timeout):
    def timed_out(signum, sigframe):
        raise RuntimeError

    old_hdl = signal.signal(signal.SIGALRM, timed_out)
    old_itimer = signal.setitimer(signal.ITIMER_REAL, timeout, 0)
    yield
    signal.setitimer(signal.ITIMER_REAL, *old_itimer)
    signal.signal(signal.SIGALRM, old_hdl)
    
if __name__ == '__main__':
    with execution_timeout(5.1):
        print 'start'
        time.sleep(5)
        print 'end'
