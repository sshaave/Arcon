#!/usr/bin/python3
from operator import itemgetter
import re
def f1(text):
    result = re.search('master="(.*)" mface',text)
    return int(result.group(1))



with open("q1.txt","r") as file:
    l = file.read()
#    print(l)
    l2=l.splitlines()
#    print(l2)
    l2.sort(key=f1)
#    print(l2)
    for x in l2:
        print(x)
#       print('\n')
#with open("y1.txt","r") as readfile:
#    types = (line.split(">") for line in readfile)
#    xys = ((type[1], type[2]) for type in types)
#    for x,y in xys:
#        print(x,y)
