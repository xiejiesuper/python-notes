# coding: utf-8
import json
import re

p = re.compile(r'\d+')
p1 = re.compile(r'\d+?')
the_str = '1a2b3c10d'
 
def f2(foo):
    data = foo.group()
    return str(int(data)+1)
 
r = p.sub(f2, the_str)
r1 = p1.sub(f2, the_str)
print r, r1
        


