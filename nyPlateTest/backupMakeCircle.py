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
# 2nd input: factor - divide this by 10
# 3rd input: depth - depth of plate
# 4th input: length - length of claw
# 5th input: ref - refine u=v
# 6th input: refW - refine W
d = int(float(sys.argv[1]))
factor = int(float(sys.argv[2]))/10
depth = int(float(sys.argv[3]))
length = int(float(sys.argv[4]))
ref = int(float(sys.argv[5]))
refW = int(float(sys.argv[6]))
#
#disc = sf.disc(r=d)
#disc2 = vf.extrude(disc, amount=(0,0,50))
#disc3=disc2.force_rational()
#with G2('G2/circleTest') as myfile4:
#        myfile4.write(disc3)
#
#lin3 = cf.line([-factor*d,factor*d],[-factor*d,-factor*d])
#prikken = cf.line([0,0],[0,0]);
prikk = cf.line([-d,0],[0,0])
prikk2=sf.revolve(prikk,theta=2*pi)
#arc2=cf.circle_segment(pi/2,r=d); arc2.rotate(3*pi/4,normal=(0,0,1))
#arc = cf.circle_segment(pi*2,r=d); arc.rotate(3*pi/4,normal=(0,0,1))
#testPrikk=sf.edge_curves(arc2,prikken)
#with G2('G2/circle1') as myfile1:
#    myfile1.write(arc)
#arcV = sf.sweep(([0,0,0],[0,0,10]),arc)
#with G2('G2/circleArc') as myfile1:
#    myfile1.write(arcV)
circPrikk = vf.extrude(prikk2,amount=(0,0,length+depth)) #; circPrikk.raise_order(1);
circPrikk.translate((0,0,-length));
circPrikk.rotate(-3*pi/4,normal=(0,0,1)); circPrikk.refine(ref,direction='u'); circPrikk.refine(ref,direction='v')
circPrikk.insert_knot((1-depth/(depth+length)),direction=2); circPrikk.raise_order(0,0,1)
#circPrikk.refine(refW,direction='w')
with G2('G2/claw') as myfile2:
    myfile2.write(circPrikk)
#with G2('G2/circle3') as myfile3:
#    myfile3.write(testPrikk)
#lin4=curve_factory.line([d,0,0],[d,0,-30])
#circ5=sf.revolve(lin4,theta=pi/2,axis=(0,0,1))
#circ5.raise_order(1)
#circ5.rotate(3*pi/4,normal=(0,0,1))
#circ5.translate((0,0,5))
#with G2('G2/circle5') as myfile5:
#    myfile5.write(circ5)
#cyl=sf.cylinder(r=10)
#with G2('G2/cyl') as myfile6:
#    myfile6.write(cyl)
#circ7temp = sf.disc(r=10); circ7temp.refine(2)
#circ7 = vf.extrude(circ7temp, amount=(0,0,20))
#with G2('G2/circ7') as myfile7:
#    myfile7.write(circ7)
#circ8 = vf.cylinder(r=10,h=20)
#with G2('G2/circ8') as myfile8:
#    myfile8.write(circ8)
