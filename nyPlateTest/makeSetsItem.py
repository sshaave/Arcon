#!/usr/bin/python3
import sys
import os
# 1st input: name of result file
# 2nd input: elNum
# 3rd input: current nx
# 4th input: current ny
# 5th input: nx
# 6th input: ny
# 7th input: face (where to constrain movement)
textFile = sys.argv[1]
elNum = int(float(sys.argv[2]))
nxTemp = int(float(sys.argv[3]))
nyTemp = int(float(sys.argv[4]))
nx = int(float(sys.argv[5]))
ny = int(float(sys.argv[6]))
face = int(float(sys.argv[7]))
if nxTemp==0 and nyTemp==0:
    with open(textFile+'.txt','w') as i2:
        i2.write('\t\t<set name="allEdges" type="face">\n')
with open(textFile+'.txt','a') as i1:
    i1.write('\t\t\t<item patch="'+str(elNum))
    i1.write('">'+str(face)+'</item>\n')
    i1.write('\t\t\t<item patch="'+str(elNum+1))
    i1.write('">'+str(face)+'</item>\n')
    i1.write('\t\t\t<item patch="'+str(elNum+2))
    i1.write('">'+str(face)+'</item>\n')
    i1.write('\t\t\t<item patch="'+str(elNum+3))
    i1.write('">'+str(face)+'</item>\n')
    if nxTemp==(nx-1) and nyTemp==(ny-1):
        i1.write('\t\t</set>\n')
