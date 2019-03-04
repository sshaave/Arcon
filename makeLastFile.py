#!/usr/bin/python3
import sys
import os
# 1st input: name of resultfile from "makeSetsItem.py"
# 2nd input: elNum of middle klakk member
nx = int(float(sys.argv[2]))
with open(sys.argv[1]+'.txt','a') as i1:
    i1.write('\t\t<set name="lastflate" type="face">\n')
    i1.write('\t\t\t<item patch="15">6</item>\n')
    i1.write('\t\t\t<item patch="19">6</item>\n')
    i1.write('\t\t\t<item patch="28">6</item>\n')
    i1.write('\t\t</set>\n')
    for x in range (1,nx-2):
        i1.write('\t\t\t<item patch="'+str(15+4*x+16*(x-1)))
        i1.write('">6</item>\n')
        i1.write('\t\t\t<item patch="'+str(15+12*x+16*(x-1)))
        i1.write('">6</item>\n')
        i1.write('\t\t</set>\n')
