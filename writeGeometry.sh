#!/bin/sh
# endret sist 19 mars kl 13

# ----- Part 1: define the problem ------
#   Define the forces
#   N = tension if positive
#   V = shear in XZ
N=112;V=0
#   Define the refinement scheme
#   refi= refinement scheme of bolt done by the scripts
#   refV = refinement in Y-dir done by the script
#   refP = polynomial refinement
refi=0;refV=0;refP=2
#   Define the geometry and refinement of the klakk
klakkLength=40;klakkY=13
klakkRefV=0;klakkRefW=0;klakkRefU=0;klakkLY=10
# claw
lengthClaw=10
#   Plate geometry definitions
xTot=180;yTot=150 #;tY1=4;tY2=2;tX1=1;tX2=3
nx=2;ny=2;d=2;depth=10;totalEle=$(( nx * ny * 4 ))
vE=$(( nx * 3 ))
n2x=$(( nx - 1 ))
nKlakk=$(( n2x * 2 ))
nKlakk=$(( nKlakk - 1 ))
# the "factor" variable is determines the thickness of the patch around the bolt hole. factor=15 equals 1.5 of d
factor=15 #this number has to be divided by 10  (workaround for bash not handling decimals)
# Calculating variables for the geometri
hE=$(( n2x * 5 ))
totalEle=$(( totalEle + nKlakk + hE + vE ))
tolX=0;tolY=0;tolBolt=0 # variables used to increase the thickness/length of the bolt hole patch
dd=0;ttol=0;d_dx=0; xTrans=0;d_dy=0
yTrans=0; l_SY=0; l_SX=0
gamma1=0; gamma1=$(( nx - 1 ))
gamma2=0; gamma2=$(( ny - 1 ))
de=$(( 2 * factor * d ))
dd=$(( de / 10 ))
ttol=$(( tolX + tolY ))
a1=0; a1=$(( nx * dd ))
b1=0; b1=$(( ttol * nx ))
c1=0; c1=$(( xTot - a1 - b1 ))
d_dx=$(( c1 / gamma1 ))
xTrans=$(( d_dx + dd + ttol ))
a2=0; a2=$(( ny * dd ))
b2=0; b2=$(( ttol * ny ))
c2=0; c2=$(( yTot - a2 - b2 ))
d_dy=$(( c2 / gamma2 ))
yTrans=$((  d_dy + dd + ttol ))
l_SY=$(( yTot - dd - dd - ttol - ttol ))
l_boltekant=$(( dd + ttol ))
klakkLX=$(( d_dx + d_dx + l_boltekant ))
a=0; elNum=0; l_SY2=$(( l_SY - klakkLY ))
# this while loop will loop over the bolts, and use python scripts to generate parts of the geometries.
# the script merge.py will simply append the new G2 file to the assembly.
# The geometry is created in the following manner: The first bolt is created, and the three parts directly above (vertically).
# then the next bolt will be created, and the parts between this bolt and the former will be created ("klakk" included). Next
# on it will create the parts verticall above itself. Finally when it reached the uppermost (always 2nd) row of bolts, it will only
# create the bolts and the horisontal parts between
while [ "$a" -lt $ny ]
do
    b=0
    while [ "$b" -lt $nx ]
    do
        # this wil make the 4 patches of the bolts
	python3 makeBolt.py $d $(( xTrans * b )) $(( yTrans * a )) $(( refi )) $(( factor )) $(( tolBolt )) $(( depth )) $refP $a
    elNum=$(( elNum + 4 ))
    #python3 makeSetsItem2.py tempFiles/setsItem $elNum $b $a $nx $ny
    python3 updatePatchFile.py tempFiles/updatePatchFile $b $a $nx $ny false $elNum
	# check if this is the first bolt. If yes, the file writer  will use 'w', else 'a'
	if [ "$a" -eq 0 ] && [ "$b" -eq 0 ]
        then
            python3 merge.py total true
        else
            python3 merge.py total false
	    # this will create the horisontal part between the bolts
            if [ "$b" -gt 0 ]
            then
		        python3 makeHorElement.py $d_dx $l_boltekant $depth $(( xTrans * b )) $(( yTrans * a )) $d $tolX $tolY $factor $b $nx $refP
                python3 merge.py total multi
                elNum=$(( elNum + 1 ))
            fi
        fi
	if [ "$a" -lt $(( ny - 1 )) ] && [ "$b" -gt 0 ]
	then
	# this will creat the middle parts (no neighbouring bolt patches)
        # first element
		python3 longSquare.py $d_dx $(( l_SY2 )) $depth $d $tolX $factor elongSq $l_boltekant $(( xTrans * b )) $xTrans $klakkLY $(( l_boltekant * 2 )) $b $nx $refP
        python3 merge.py total middleSquares
        elNum=$(( elNum + 1 ))
        # second element, this will be directly under the klakk
        deltaYpgaKlakk=1
        python3 longSquare.py $d_dx $(( 2 * klakkLY )) $depth $d $tolX $factor elongSq $l_boltekant $(( xTrans * b )) $xTrans $klakkLY $(( l_boltekant + l_boltekant + l_SY2 )) $b $nx $refP
        python3 merge.py total middleSquares
        elNum=$(( elNum + 1 ))
	    tempNum=$(( totalEle - nx + b ))
        # make the klakk which is places over the middle squares
        if [ "$b" -gt 0 ] && [ "$b" -lt $nx ]
        then
            tempTransX=$(( xTrans * b ))
            python3 makeKlakk.py $l_boltekant $(( tempTransX - d_dx )) $l_SY2 $klakkRefU $klakkRefV $klakkRefW $d_dx $klakkLY $factor $d $tolBolt $depth $b $nx $refP $klakkLength
            python3 merge.py total klakk
            elNum=$(( elNum + 1 ))
        fi
        # third element, this will be the uppermost of the middle squares
        deltaYpgaKlakk=$(( l_boltekant + l_boltekant + l_SY2 + klakkLY + klakkLY ))
        python3 longSquare.py $d_dx $(( l_SY2 )) $depth $d $tolX $factor elongSq $l_boltekant $(( xTrans * b )) $xTrans $klakkLY $(( deltaYpgaKlakk )) $b $nx $refP
	    python3 merge.py total middleSquares
        elNum=$(( elNum + 1 ))
    fi
	if [ "$a" -lt $(( ny - 1 )) ]
	then
		# this will create the vertical parts between the bolts
		python3 smallMulti.py $l_boltekant $l_SY2 $depth $(( xTrans * b )) $(( 2 * yTrans * a )) $d $tolX $tolY $factor $klakkLY $refV $refP
		python3 merge.py total multi
        elNum=$(( elNum + 1 ))
        # nr 2
        python3 smallMulti.py $l_boltekant $(( 2 * klakkLY )) $depth $(( xTrans * b )) $l_SY2 $d $tolX $tolY $factor $klakkLY $refV $refP
        python3 merge.py total multi
        elNum=$(( elNum + 1 ))
		if [ "$b" -gt 0 ] && [ "$b" -lt $n2x ]
		then
            # make the klakk which is places over the vertical parts
	    	python3 makeKlakk.py $l_boltekant $(( xTrans * b )) $l_SY2 $(( klakkRefU )) $klakkRefV $klakkRefW $l_boltekant $klakkLY $factor $d $tolBolt $depth 0 $nx $refP $klakkLength
            elNum=$(( elNum + 1 ))
            python3 merge.py total klakk
		fi
        # nr 3
        python3 smallMulti.py $l_boltekant $l_SY2 $depth $(( xTrans * b )) $(( l_SY2 + klakkLY + klakkLY )) $d $tolX $tolY $factor $klakkLY $refV $refP
        python3 merge.py total multi
        elNum=$(( elNum + 1 ))
	fi
        b=$(( b + 1 ))
    done
    a=$(( a + 1 ))
done

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
