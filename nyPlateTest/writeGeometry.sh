#!/bin/sh
# endret sist 15 des kl 13

avstandY=7
avstandX=14

# ----- Part 1: define the problem ------
#   Define the forces
#   N = tension if positive
#   V = shear in XZ
N=10;V=0
#   Define the refinement scheme
#   refi= refinement scheme of bolt done by the scripts
#   refV = refinement in Y-dir done by the script
#   refP = polynomial refinement
refi=0;refV=0;refP=2
#   Define the geometry and refinement of the klakk, klakkLength=height Z-dir
# claw
lengthClaw=5
#   Plate geometry definitions
xTot=250;yTot=200 #;tY1=4;tY2=2;tX1=1;tX2=3
nx=1;ny=1;d=12;depth=5;totalEle=$(( nx * ny * 4 ))
tolX=0;tolY=0
vE=$(( nx * 3 ))
n2x=$(( nx - 1 ))
nKlakk=$(( n2x * 2 ))
nKlakk=$(( nKlakk - 1 ))
# the "factor" variable is determines the thickness of the patch around the bolt hole. factor=15 equals 1.5 of d
factor=15 #this number has to be divided by 10  (workaround for bash not handling decimals)
# Calculating variables for the geometri
hE=$(( n2x * 5 ))
totalEle=$(( totalEle + nKlakk + hE + vE ))
dd=0;ttol=0;d_dx=0; xTrans=0;d_dy=0
yTrans=0; l_SY=0; l_SX=0
gamma1=0; gamma1=$(( nx ))
gamma2=0; gamma2=$(( ny ))
de=$(( 2 * factor * d ))
dd=$(( de / 10 ))

a1=0; a1=$(( nx * dd ))
b1=0; b1=$(( ttol * nx ))
c1=0; c1=$(( xTot - a1 - b1 ))
d_dx=$(( c1 / gamma1 ))

a2=0; a2=$(( ny * dd ))
b2=0; b2=$(( ttol * ny ))
c2=0; c2=$(( yTot - a2 - b2 ))
d_dy=$(( c2 / gamma2 ))
yTrans=$((  d_dy + dd + ttol ))
l_SY=$(( yTot - dd - dd - ttol - ttol ))
l_boltekant=$(( dd + ttol ))
avstand2X=$(( 42 - l_boltekant ))
avstandX=$(( avstand2X / 2 ))
avstand2Y=$(( 56 - l_boltekant ))
avstandY=$(( avstand2Y / 2 ))
#l_boltekant=24
klakkLX=$(( d_dx + d_dx + l_boltekant ))
a=0; elNum=0; l_SY2=$(( l_SY - klakkLY ))
# this while loop will loop over the bolts, and use python scripts to generate parts of the geometries.
# the script merge.py will simply append the new G2 file to the assembly.
# The geometry is created in the following manner: The first bolt is created, and the three parts directly above (vertically).
# then the next bolt will be created, and the parts between this bolt and the former will be created ("klakk" included). Next
# on it will create the parts verticall above itself. Finally when it reached the uppermost (always 2nd) row of bolts, it will only

# l_boltekant = dd + ttol = dd + 0 = 

# create the three first elements
python3 makeHorElement.py $avstandX $avstandY $depth $(( 0* l_boltekant )) $(( -1 * avstandY )) $d $tolX $tolY $factor 0 1 $refP
python3 merge.py total multi2
python3 makeHorElement.py $l_boltekant $avstandY $depth $(( 1* l_boltekant )) $(( -1 * avstandY )) $d 0 0 $factor 0 1 $refP
python3 merge.py total multi
python3 makeHorElement.py $avstandX $avstandY $depth $(( avstandX + l_boltekant )) $(( -1 * avstandY )) $d $tolX $tolY $factor 0 $nx $refP
python3 merge.py total multi
# create the patch left to the bolt
python3 makeHorElement.py $avstandX $l_boltekant $depth $(( 0* l_boltekant )) $(( 0 * l_boltekant )) $d $tolX $tolY $factor 0 $nx $refP
python3 merge.py total multi

# create the first middle bolt
python3 makeSingleBolt.py $d 0 0 $(( refi )) $(( factor )) $(( tolBolt )) $depth $refP
python3 merge.py total true
# create the patch right to the bolt
python3 makeHorElement.py $avstandX $l_boltekant $depth $(( avstandX + l_boltekant )) $(( 0 * l_boltekant )) $d $tolX $tolY $factor 0 $nx $refP
python3 merge.py total multi

# create the three first elements
python3 makeHorElement.py $avstandX $avstandY $depth $(( 0* l_boltekant )) $(( 1 * l_boltekant )) $d $tolX $tolY $factor 0 $nx $refP
python3 merge.py total multi
python3 makeHorElement.py $l_boltekant $avstandY $depth $(( 1* l_boltekant )) $(( 1 * l_boltekant )) $d $tolX $tolY $factor 0 $nx $refP
python3 merge.py total multi
python3 makeHorElement.py $avstandX $avstandY $depth $(( avstandX + l_boltekant )) $(( 1 * l_boltekant )) $d $tolX $tolY $factor 0 $nx $refP
python3 merge.py total multi


# make the 3 last parts


# make the claws
a=0
lowerBolt=0;lowerBolt=$elNum
while [ "$a" -lt $ny ]
do
    b=0
    while [ "$b" -lt $nx ]
    do
    	python3 makeCircle.py $d $(( xTrans * b )) $(( yTrans * a )) $factor $depth $lengthClaw 1 1
    	python3 merge.py total claw
        python3 makeSetsItem.py tempFiles/setsItem $(( elNum + 1 )) $b $a $nx $ny 5
        elNum=$(( elNum + 4 ))
	b=$(( b + 1 ))
    done
    a=$(( a + 1 ))
done
upperBolt=$elNum
# update the .xinp with the claw

#

# This will create a intermediate textfile used in the <connection> setting
python3 makeLoadFile.py tempFiles/setsItem $nx
echo Wrap it up
# Wrap it up
../../Mappe/IFEM-GPM/bin/./getGNO -v G2/total.g2 | grep "<connection" > tempFiles/patchFileTemp.txt
python3 qMerge.py
python3 qSort.py
python3 makeFile.py resultat.xinp G2/total.g2 tempFiles/setsItem.txt $N $V $elNum $lowerBolt $upperBolt 3 3 3
echo $elNum
echo $l_boltekant
