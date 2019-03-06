#!/usr/bin/python3
from operator import itemgetter
import re
def f1(text):
    result = re.search('master="(.*)" mface',text)
    return int(result.group(1))

with open('hei123.txt','r') as file:
    l = file.read()
    l2=l.splitlines()
    l2.sort(key=f1)
    with open('con.txt','w') as con:
        for x in l2:
            con.write(x+'\n')

