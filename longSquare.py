#!/usr/bin/python3
#This script will create the elongated square between the two row of bolts
import sys
from sys import path
path.append('../../Mappe/Splipy/')
from splipy import *
import splipy.curve_factory as cf
import splipy.surface_factory as sf
import splipy.volume_factory as vf
import numpy as np
np.set_printoptions(precision=6)
from splipy.io import G2
from math import pi
# 1st input: xLength
# 2nd input: yLength*2
# 3rd input: depth
# 4th input: d bolt diameter
# 5th input: tolX
# 6th input: factor
# 7th input: name of G2-file
# 8th input: l_boltekant
# 9th input: deltaX
# 10th input: deltaX pr bolt
# 11th input: klakkLY
# 12th input: deltaYpgaKlakk
# 13th input: b, tellevariabel for nx
# 14th input: nx
# 15th input: refP
xL = int(float(sys.argv[1]))
yL = float(sys.argv[2])/2
depth = int(float(sys.argv[3]))
d = int(float(sys.argv[4]))
tol = int(float(sys.argv[5]))
factor = float(sys.argv[6])/10
l_boltekant = int(float(sys.argv[8]))
DELTA_X = int(float(sys.argv[9]))
modXX = int(float(sys.argv[10]))
klakkLY = float(sys.argv[11])
dYKlakk = float(sys.argv[12])/2
b = int(float(sys.argv[13]))
nx = int(float(sys.argv[14]))
refP = int(float(sys.argv[15]))
#xxL - l_boltekant*2
square1 = sf.square(size=(xL,yL))
#square1.raise_order(refP)
sq1 = vf.extrude(square1,amount=(0,0,depth))
# Refinements. k-refinement is preferred, and is achieved by order elevation before knot insertions
sq1.raise_order(refP)
#sq1.refine(1)
if b==1:
    sq1.insert_knot(0.15,direction=0)
elif b==(nx-1):
    sq1.insert_knot(0.85,direction=0)
sq1.refine(1,direction='u') #3
if yL > klakkLY + 1:
    sq1.refine(1,direction='v')
else:
    sq1.refine(1,direction='v')
#sq1.refine(2,direction='w')
# make the knot insertion at the point of the klakk
#lower = 0.5 - klakkLY/(yL*2)
#upper = 0.5 + klakkLY/(yL*2)
#sq1.insert_knot(lower,direction=1)
#sq1.insert_knot(upper,direction=1)
#sq1.insert_knot(0.5,direction=1)
#
#-6,9 = -2d-tol; 2d+tol
deltaX = factor*d + tol
modX= -(modXX)
#deltaY =  9
sq1.translate((deltaX,-deltaX,0))
sq1.translate((DELTA_X,dYKlakk,0))
sq1.translate((modX,0,0))
with G2('G2/'+sys.argv[7]) as myfile:
    myfile.write(sq1)

