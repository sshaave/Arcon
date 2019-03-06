
#!/usr/bin/python3
import sys
import os
name = sys.argv[1]
patchName = sys.argv[2]
topFile = sys.argv[3]
top2File='hei123.txt'
setFile = sys.argv[4]
strekk = sys.argv[5]
V = sys.argv[6]
elNum=int(float(sys.argv[7]))
refU=sys.argv[8]
refV=sys.argv[9]
refW=sys.argv[10]
with open(name,'w') as i1:
    i1.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n\n')
    i1.write('<!-- automatically generated file from script for Arcon Prosjekt AS. !-->\n\n')
    i1.write('<simulation>\n\n')
    i1.write('<!-- Geometry definitions -->\n')
    i1.write('<geometry>\n')
    i1.write('\t<patchfile>'+ patchName + '</patchfile>\n')
#    for i in range(elNum):
#        i1.write('\t<refine patch="'+str(i+1))
#        i1.write('" u="'+refU)
#        i1.write('" v="'+refV)
#        i1.write('" w="'+refW)
#        i1.write('"/>\n')
    i1.write('\t<refine lowerpatch="1" u="'+refU)
    i1.write('" v="'+refV)
    i1.write('" w="'+refW)
    i1.write('"/>\n')
#    with open(topFile,'rb') as t1:
    i1.write('\t<topology>\n')
    for line in reversed(list(open(topFile))):
        i1.write("\t")
        i1.write(line.rstrip())
        i1.write("\n")
    with open(top2File) as t2:
        for line in t2:
            i1.write("\t"+line)
    i1.write('\t</topology>\n')
    i1.write('\t<topologysets>\n')
    with open(setFile) as t3:
        for line in t3:
            i1.write(line)
    i1.write('\t</topologysets>\n')
    i1.write('</geometry>\n\n')
    i1.write('<!-- Gauss quadrature scheme !-->\n')
    i1.write('<discretization>\n')
    i1.write('\t<nGauss default="0"/>\n')
    i1.write('</discretization>\n\n')
    i1.write('<!-- Boundary conditions !-->\n')
    i1.write('<boundaryconditions>\n')
    i1.write('\t<dirichlet set="allEdges" comp="123"/>\n')
    i1.write('\t<neumann set="lastflate" direction="3" type="constant">'+strekk)
    i1.write('</neumann>\n')
    i1.write('\t<neumann set="lastflate" direction="1" type="constant">'+V)
    i1.write('</neumann>\n')
    i1.write('</boundaryconditions>\n\n')
    i1.write('<!-- Problem specific block !-->\n')
    i1.write('<elasticity>\n')
    i1.write('\t<isotropic E="2.1e5" nu="0.3" rho="7850e-6"/>\n')
    i1.write('</elasticity>\n\n')
#    i1.write('<!-- Post processing !-->\n')
#    i1.write('<postprocessing>\n')
#    i1.write('\t<vtfformat>BINARY</vtfformat>\n')
#    i1.write('<projection>\n')
#    i1.write('\t<cgl2/>\n')
#    i1.write('</projection>\n')
#    i1.write('</postprocessing>\n\n')
    i1.write('</simulation>')
