# -*- coding: utf-8 -*-
import os, sys, time, subprocess
from threading import Thread

ISOTIMEFORMAT = '%Y-%m-%d %X'


# 程序功能部分
def main():
    raw_input()   # 模拟监听请求


class MainThread(Thread):
    
    def __init__(self):
        super(MainThread, self).__init__()
        
    def run(self):
        main()

        
def autoreload(path):
    '''
    from autoreload import autoreload
    path = os.path.abspath(__file__)
    autoreload(path)
    '''
    # 当前文件路径
    path = path or os.path.abspath(__file__)

    # 当前文件修改时间
    mtime = os.stat(path).st_mtime
    # 主进程为控制器，不做功能处理
    if not os.environ.get('is_child'):
        argv = [sys.executable] + sys.argv
        environ = os.environ.copy()

        # 给子进程标记，不做控制功能
        environ['is_child'] = 'true'

        # 先开一个子进程，执行程序功能
        subprocess.Popen(argv, env=environ)

        while True:
            if os.stat(path).st_mtime != mtime:
                mtime = os.stat(path).st_mtime
                subprocess.Popen(argv, env=environ)
                print '**reloaded ' + time.strftime(ISOTIMEFORMAT, time.localtime()) +\
                    '\n********************************'

            time.sleep(1)

    # 新线程执行功能
    MainThread().start()
