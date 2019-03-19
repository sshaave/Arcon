#!/usr/bin/python3
#kan ikke bruke 15, regn denne ut! 15 = 5nx hvis nx=3
import sys
import os
patchName = sys.argv[1]
nx = int(float(sys.argv[2]))
ny = int(float(sys.argv[3]))
nxTot = int(float(sys.argv[4]))
nyTot = int(float(sys.argv[5]))
elNum = int(float(sys.argv[7]))
#if ny==0 and nx ==0:
#    with open(patchName+'.txt','a') as i1:
#        i1.write('<topology>\n')
if nx==0 and ny==0:
    with open(patchName+'.txt','w') as i1:  # Handle the first vertical element and the first hor element
        i1.write('\t<connection master="5" mface="3" slave="1" sface="3" orient="2"/>\n')
        i1.write('\t<connection master="12" mface="1" slave="4" sface="3"/>\n')
        tempNum = 13*nxTot-3
        i1.write('\t<connection master="'+str((tempNum+5)))
        i1.write('" mface="1" slave="'+str((tempNum)))
        i1.write('" sface="3"/>\n')
elif ny==0:                                       # Handle the next vertical elements
    tempNum = 8 + (nx-1)*11 + 2*(nx-1)
    with open(patchName+'.txt','a') as i1:
        i1.write('\t<connection master="'+str((tempNum+9)))
        i1.write('" mface="3" slave="'+str((tempNum)))
        i1.write('" sface="3" orient="2"/>\n')
if nx>0 and ny==0:
    with open(patchName+'.txt','a') as i1: # Handle the horisontal elements except the first ones
        if (nx<(nxTot-1)):
            i1.write('\t<connection master="'+str((elNum+14)))
            i1.write('" mface="1" slave="'+str((elNum)))
            i1.write('" sface="3"/>\n')
        i1.write('\t<connection master="'+str((elNum+1)))
        i1.write('" mface="2" slave="'+str((elNum-2)))
        i1.write('" sface="3" orient="2"/>\n')
elif nx>0 and ny==1:
    with open(patchName+'.txt','a') as i1:
        i1.write('\t<connection master="'+str((elNum+1)))
        i1.write('" mface="2" slave="'+str((elNum-2)))
        i1.write('" sface="3" orient="2"/>\n')
        if nx <(nxTot-1):
            i1.write('\t<connection master="'+str((elNum+6)))
            i1.write('" mface="1" slave="'+str((elNum)))
            i1.write('" sface="3"/>\n')
if sys.argv[6] == 'true':
    with open(patchName+'.txt','a') as i1:
        i1.write('</topology>')
