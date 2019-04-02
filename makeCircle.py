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
# handle input
# 1st input: d - diameter of bolt/claw
# 2nd input: transX
# 3rd input: transY
# 4th input: factor - divide this by 10
# 5th input: depth - depth of plate
# 6th input: length - length of claw
# 7th input: refV - refine v
# 8th input: refW - refine W
d = int(float(sys.argv[1]))
transX = int(float(sys.argv[2]))
transY = int(float(sys.argv[3]))
factor = int(float(sys.argv[4]))/10
depth = int(float(sys.argv[5]))
length = int(float(sys.argv[6]))
refRad = int(float(sys.argv[7]))
refW = int(float(sys.argv[8]))
refT=0
#
prikk = cf.line([-d,0],[0,0])
prikk2=sf.revolve(prikk,theta=pi/2)
c1 = vf.extrude(prikk2,amount=(0,0,-length)); c1.raise_order(1,1,0);
c1.translate((0,0,depth));
c1.rotate(-3*pi/4,normal=(0,0,1)); c1.refine(refRad,direction='u'); c1.refine(refT,direction='v')
#c1.insert_knot((depth/(depth+length)),direction=2);
c1.raise_order(0,0,2)

c2 = vf.extrude(prikk2,amount=(0,0,-length)); c2.raise_order(1,1,0);
c2.translate((0,0,depth));
c2.rotate(-3*pi/4,normal=(0,0,1)); c2.refine(refRad,direction='u'); c2.refine(refT,direction='v')
#c2.insert_knot((depth/(depth+length)),direction=2)
c2.raise_order(0,0,2); c2.rotate(pi/2,normal=(0,0,1))

c3 = vf.extrude(prikk2,amount=(0,0,-length)); c3.raise_order(1,1,0);
c3.translate((0,0,depth));
c3.rotate(-3*pi/4,normal=(0,0,1)); c3.refine(refRad,direction='u'); c3.refine(refT,direction='v')
#c3.insert_knot((depth/(depth+length)),direction=2);
c3.raise_order(0,0,2); c3.rotate(pi,normal=(0,0,1))

c4 = vf.extrude(prikk2,amount=(0,0,-length)); c4.raise_order(1,1,0);
c4.translate((0,0,depth));
c4.rotate(-3*pi/4,normal=(0,0,1)); c4.refine(refRad,direction='u'); c4.refine(refT,direction='v')
#c4.insert_knot((depth/(depth+length)),direction=2);
c4.raise_order(0,0,2); c4.rotate(3*pi/2,normal=(0,0,1))
if transX > 0 or transY > 0:
    c1.translate((transX,transY,0))
    c2.translate((transX,transY,0))
    c3.translate((transX,transY,0))
    c4.translate((transX,transY,0))

with G2('G2/claw1') as myfile1:
    myfile1.write(c1)
with G2('G2/claw2') as myfile2:
    myfile2.write(c2)
with G2('G2/claw3') as myfile3:
    myfile3.write(c3)
with G2('G2/claw4') as myfile4:
    myfile4.write(c4)
