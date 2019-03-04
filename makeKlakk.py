#!/usr/bin/python3
import sys
from sys import path
path.append('../../Mappe/Splipy/')
from splipy import *
import splipy.surface_factory as sf
import splipy.volume_factory as vf
import numpy as np
from splipy.io import G2
from math import pi
# 1st input: l_boltekant
# 2nd input: placement from first bolt corner X-dir
# 3rd input: placement from first bolt corner Y-dir
# 4th input: refinement in u
# 5th input: refinement in v
# 6th input: refinement in w
# 7th input: klakk length X-dir
# 8th input: klakk length Y-dir
# 9th input: factor
# 10th input: bolt diameter d
# 11th input: tolBolt
# 12th input: plateDepth
# 13th input: tellevariabel for nx
# 14th input: nx
# 15th input: refP
#Handling input
l_boltekant = int(float(sys.argv[1]))
delX = int(float(sys.argv[2])) # l_boltekant
delYY = int(float(sys.argv[3])) # l_SY
refU = int(float(sys.argv[4]))
refV = int(float(sys.argv[5]))
refW = int(float(sys.argv[6]))
lX = int(float(sys.argv[7]))
lY = float(sys.argv[8])
factor = int(float(sys.argv[9]))/10
d = int(float(sys.argv[10]))
tolBolt = int(float(sys.argv[11]))
pDepth = int(float(sys.argv[12]))
bNx = int(float(sys.argv[13]))
nx = int(float(sys.argv[14]))
refP = int(float(sys.argv[15]))
#
dX = factor*d + tolBolt
s1 = sf.square(size=(lX,lY))
#s1.raise_order(refP)
v1 = vf.extrude(s1,amount=(0,0,6))
v1.raise_order(refP)
#
l_SY = delYY
delY = l_SY/2 + l_boltekant
#
v1.translate((-dX,-dX,pDepth))
v1.translate((delX,delY,0))
#v1.raise_order(1)
#locally refining
v1.insert_knot(0.125,direction=2)
if bNx==1:
    v1.insert_knot(0.15,direction=0)
elif bNx==(nx-1):
    v1.insert_knot(0.85,direction=0)
#refining
v1.refine(refU,direction='u')
v1.refine(refV,direction='v')
v1.refine(refW,direction='w')

with G2('G2/klakk') as myfile1:
    myfile1.write(v1)

