#!/usr/bin/python3
from operator import itemgetter
import re
import os
import sys
# 1st input: name of connection file from getGNO
# 2nd input: name of 2nd connection file
# 3rd input: name of output file
file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]
with open(file3,'w') as f3:
    with open(file1,'r') as f1:
        for line in f1:
	    f3.write(line)
	with open(file2,'r') as f2:
	    for line in f2:
	        f3.write(line)

def f1(text):
    result = re.search('master="(.*)" mface',text)
    return int(result.group(1))

with open(file3,"r") as file:
    l = file.read()
    l2=l.splitlines()
    l2.sort(key=f1)
    with open('con.txt','r') as con:
        for x in l2:
            con.write(x)

