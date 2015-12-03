# -*- coding: utf-8 -*-
import unittest


# 方法1
class Singleton(type):
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None
        
    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance
        
        
# 方法2
class Singleton1(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton1, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance
        
        
# 方法3
class Singleton2(object):
    _state = {}
    
    def __new__(cls, *args, **kw):
        ob = super(Singleton2, cls).__new__(cls, *args, **kw)
        ob.__dict__ = cls._state
        return ob
        
        
# 方法4
def singleton3(cls, *args, **kw):
    instances = {}
    
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton
    
    
# test
class TestCase(unittest.TestCase):
    def testSingleton(self):
        class TestSingleton(object):
            __metaclass__ = Singleton
        a = TestSingleton()
        b = TestSingleton()
        self.assertEqual(id(a) == id(b), True)
    
    def testSingleton1(self):
        class TestSingleton(Singleton1):
            pass
        a = TestSingleton()
        b = TestSingleton()
        self.assertEqual(id(a) == id(b), True)
    
    def testSingleton2(self):
        class TestSingleton(Singleton2):
            pass
        a = TestSingleton()
        b = TestSingleton()
        self.assertEqual(id(a.__dict__) == id(b.__dict__), True)
    
    def testSingleton3(self):
        @singleton3
        class TestSingleton(object):
            pass
        a = TestSingleton()
        b = TestSingleton()
        self.assertEqual(id(a) == id(b), True)
        
        
if __name__ == '__main__':
    unittest.main()
