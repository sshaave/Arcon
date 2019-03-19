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
# 1st input: plate dimension in X
# 2nd input: outer element in X thickness
# 3rd input: plate dimension in Y
# 4th input: outer element in Y thickness
# 5th input: depth
# 6th input: factor, divide this by 10 to circumvent float/int issue in bash
# 7th input: tolX
# 8th input: tolY
# 9th input: tolBolt
# 10th input: refinement
# 11th input: bolt diameter
# 12th input: thickness of upper piece along x
# 13th input: thickness of right piece along y
# 14th input: "inner" length in Y
#Handling input
xL = int(float(sys.argv[1]))
tX1 = int(float(sys.argv[2]))
yL = int(float(sys.argv[3]))
tY1 = int(float(sys.argv[4]))
depth = int(float(sys.argv[5]))
factor = float(sys.argv[6])/10
tolX = int(float(sys.argv[7]))
tolY = int(float(sys.argv[8]))
tolBolt = int(float(sys.argv[9]))
refi = int(float(sys.argv[10]))
d = int(float(sys.argv[11]))
tX2 = int(float(sys.argv[12]))
tY2 = int(float(sys.argv[13]))
yTot= int(float(sys.argv[14]))
#lengthYInY = yL - tX1 - tX2
#Creating the two parts (x and Y)
sX = sf.square(size=(xL,tX1))
sY = sf.square(size=(tY1,yTot))
sX2 = sf.square(size=(xL,tX2))
sY2 = sf.square(size=(tY2,yTot))
sqX = vf.extrude(sX,amount=(0,0,depth))
sqY = vf.extrude(sY,amount=(0,0,depth))
sqX2= vf.extrude(sX2,amount=(0,0,depth))
sqY2= vf.extrude(sY2,amount=(0,0,depth))
# k-refinements
sqX.raise_order(1)
sqY.raise_order(1)
sqX2.raise_order(1)
sqY2.raise_order(1)
sqX.refine(refi,direction='u');sqX.refine(refi,direction='v')
sqY.refine(refi,direction='u');sqY.refine(refi,direction='v')
sqX2.refine(refi,direction='u');sqX2.refine(refi,direction='v')
sqY2.refine(refi,direction='u');sqY2.refine(refi,direction='v')
# placing the first element in x
xDeltaX = -factor*d - tolBolt -tY1
xDeltaY = -factor*d - tolBolt -tX1
sqX.translate((xDeltaX,xDeltaY,0))
# placing the fist element in y
yDeltaX = xDeltaX
yDeltaY = -factor*d - tolBolt
sqY.translate((yDeltaX,yDeltaY,0))
# placing the second element in x
sqX2.translate((xDeltaX,xDeltaY,0))
deltaSqX2 = yTot + tX1
sqX2.translate((0,deltaSqX2,0))
#placing the second element in y
sqY2.translate((yDeltaX,yDeltaY,0))
deltaSqY2 = xL - tY2
sqY2.translate((deltaSqY2,0,0))

with G2('G2/firstX') as myfile1:
    myfile1.write(sqX)
with G2('G2/firstY') as myfile2:
    myfile2.write(sqY)
with G2('G2/secondX') as myfile3:
    myfile3.write(sqX2)
with G2('G2/secondY') as myfile4:
    myfile4.write(sqY2)
# moving the two objects to their 2nd positon around the plate
#xTransY = yL - tX
#yTransX = xL - tY
#sqX.translate((0,xTransY,0))
#sqY.translate((yTransX,0,0))
#with G2('G2/secondX') as myfile3:
#    myfile3.write(sqX)
#with G2('G2/secondY') as myfile4:
#    myfile4.write(sqY)
