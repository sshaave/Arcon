#!/usr/bin/python3
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
# 1st input: diameter
# 2nd input: translation in X-dir
# 3rd input: translation in Y-dir
# 4th input: refinement
# 5th input: factor
# 6th input: tol
# 7th input: depth
# 8th input: ref pol-degree
# 9th input: tellevariabel for ny
# handling input variables, converting from string to int
d = int(float(sys.argv[1]))
distX = int(float(sys.argv[2]))
distY = int(float(sys.argv[3]))
refi = int(float(sys.argv[4]))
factor = float(sys.argv[5])/10
tol = int(float(sys.argv[6]))
depth = int(float(sys.argv[7]))
refP = int(float(sys.argv[8]))
a = int(float(sys.argv[9]))
#
line3 = cf.line([-factor*d-tol,factor*d+tol], [-factor*d-tol,-factor*d-tol])
arc = cf.circle_segment(pi/2,r=d)
arc.rotate(3*pi/4, normal=(0,0,1))
surf = sf.edge_curves(line3,arc)
surf.rotate(3*pi/2, normal=(0,0,1))
#
s1 = vf.extrude(surf, amount=(0,0,depth))
s1.raise_order(refP-1,refP-1,refP)
#s1.refine(1)
#s1.raise_order(1)
if a == 30000:
    s1.refine(refi+1,direction='u')
else:
    s1.refine(refi,direction='u')
s1.refine(refi+1,direction='v')
#
s2 = vf.extrude(surf, amount=(0,0,depth))
s2.raise_order(refP-1,refP-1,refP)
s2.refine(refi,direction='u')
s2.refine(refi+1,direction='v')
s2.rotate(pi/2,normal=(0,0,1))
#
s3 = vf.extrude(surf,amount=(0,0,depth))
s3.raise_order(refP-1,refP-1,refP)
if a==10000:
    s3.refine(refi+1,direction='u')
else:
    s3.refine(refi,direction='u')
s3.refine(refi+1,direction='v')
s3.rotate(pi,normal=(0,0,1))
#
s4 = vf.extrude(surf,amount=(0,0,depth))
s4.raise_order(refP-1,refP-1,refP)
s4.refine(refi,direction='u')
s4.refine(refi+1,direction='v')
s4.rotate(3*pi/2,normal=(0,0,1))

if distX > 0 or distY > 0:
    s1.translate((distX,distY,0))
    s2.translate((distX,distY,0))
    s3.translate((distX,distY,0))
    s4.translate((distX,distY,0))
with G2('G2/1Test') as myfile1:
        myfile1.write(s1)
with G2('G2/2Test') as myfile2:
        myfile2.write(s2)
with G2('G2/3Test') as myfile3:
        myfile3.write(s3)
with G2('G2/4Test') as myfile4:
        myfile4.write(s4)
