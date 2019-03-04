#!/usr/bin/python3
#This script will create the small elongated squared between the bolts and the mid square, y-dir
import sys
from sys import path
path.append('../../Mappe/Splipy/')
from splipy import *
import splipy.surface_factory as sf
import splipy.volume_factory as vf
import numpy as np
np.set_printoptions(precision=6)
from splipy.io import G2
from math import pi
# 1st input: xLength
# 2nd input: yLength
# 3rd input: depth
# 4th input: dX
# 5th input: dY
# 6th input: d
# 7th input: tolX
# 8th input: tolY
# 9th input: factor
# 10th input: klakkLY
# 11th input: refV
# 12th input:refP
xL = int(float(sys.argv[1])) # l_boltekant
yL = float(sys.argv[2])/2 # l_SY2
depth = int(float(sys.argv[3]))
dX = int(float(sys.argv[4]))
dY = int(float(sys.argv[5]))/2 # avoid float/int
d = int(float(sys.argv[6]))
xTol = int(float(sys.argv[7]))
yTol = int(float(sys.argv[8]))
factor = float(sys.argv[9])/10
klakkLY = int(float(sys.argv[10]))
refV = int(float(sys.argv[11]))
refP = int(float(sys.argv[12]))
#
square1 = sf.square(size=(xL,yL))
#square1.raise_order(refP)
sq1 = vf.extrude(square1, amount=(0,0,depth))
sq1.raise_order(refP)
sq1.refine(1,direction='u') #2
if yL > klakkLY + 1:
    sq1.refine(refV,direction='v') #2
else:
    sq1.refine(1,direction='v')
#sq1.refine(2,direction='w')
# make the knot insertion at the point of the klakk
#lower = 0.5 - klakkLY/(yL*2)
#lower1 = (0.5 + lower)/2
#upper = 0.5 + klakkLY/(yL*2)
#upper1 = (0.5 + upper)/2
#sq1.insert_knot(0.5,direction=1)
#sq1.insert_knot(0.45,direction=1)
#sq1.insert_knot(lower1,direction=1)
#sq1.insert_knot(0.55,direction=1)
#sq1.insert_knot(upper1,direction=1)
#
modX = factor*d + xTol
modY = factor*d + yTol
sq1.translate((dX,dY,0))
sq1.translate((modX,modY,0))
sq1.translate((-xL,0,0))

with G2('G2/litenMulti') as myfile:
    myfile.write(sq1)
