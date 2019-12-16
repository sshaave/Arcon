# Arcon
Plateknekking


These scripts intention is to recieve input from a user in Windows OS using Excel via cmd/terminal. The specifics
of the code will not be available to the user. If, however, someone wishes to understand what this scripts does,
a brief explanation will be given: 

The master scrips is named "testScript.sh" and is a shell script. It recives input from Excel, and calculates the 
sized of the different patches. The script will loop through the bolts, nx and ny, and will work relatively around
the bolts. Firstly it produces the 4 patches of the bolts, merges it into the same G2 file, and continues on with 
the neighbouring vertical and horisontal elements. Bolt patches -> the elements above (mening between the two 
horisontal bolt rows) with klakk -> the horisontal elemnts to the sides. The geometry is merged to the "total.g2" 
file after every step. myPython.py produces the bolt patches; longSquare.py produces the middle elements which has no 
neighbouring bolts; smallMulti.py produces the verical elemnts with klakks (or none) on; makeKlakk produces the "klakk
"; 2smallMulti.py produces the horisontal elements between the bolts. 

Next on is to determine the connection tags, which will be stored temporarily in "patchTempFile.txt" and "hei123.txt"
-glorius name-. Same with the set tags. In order to do this, a variable elNum is used. getGNO is used to automatically
find a lot of the connections. This is done by updatePatchFile.py, qSort.py.


Then it is time to write the input-file for IFEM. Done by makeFile.py. 
