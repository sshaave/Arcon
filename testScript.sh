#!/bin/sh
# 28feb kl 16
echo ls
N=2000;V=500
refi=1; refVmidtre=1; refV=1;refP=2
factor=15 #this number has to be divided by 10  (workaround for bash not handling decimals)
lengthX=60;lengthY=34;klakkLength=15;klakkY=13;klakkRefV=1;klakkRefW=0;klakkRefU=1;klakkLY=1
xTot=54;yTot=30;tY1=4;tY2=2;tX1=1;tX2=3
nx=3;ny=2;d=2;depth=3;totalEle=$(( nx * ny * 4 ))
vE=$(( nx * 3 ))
n2x=$(( nx - 1 ))
nKlakk=$(( n2x * 2 ))
nKlakk=$(( nKlakk - 1 ))
#echo $nKlakk
hE=$(( n2x * 5 ))
totalEle=$(( totalEle + nKlakk + hE + vE ))
tolX=0;tolY=0;tolBolt=0
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
	python3 myPython.py $d $(( xTrans * b )) $(( yTrans * a )) $(( refi )) $(( factor )) $(( tolBolt )) $(( depth )) $refP
    elNum=$(( elNum + 4 ))
    python3 makeSetsItem.py setsItem $elNum $b $a $nx $ny
    python3 updatePatchFile.py hei123 $b $a $nx $ny false $elNum
	# check if this is the first bolt. If yes, the file writer  will use 'w', else 'a'
	if [ "$a" -eq 0 ] && [ "$b" -eq 0 ]
        then
            python3 merge.py total true
        else
            python3 merge.py total false
	    # this will create the horisontal part between the bolts
            if [ "$b" -gt 0 ]
            then
		        python3 2smallMulti.py $d_dx $l_boltekant $depth $(( xTrans * b )) $(( yTrans * a )) $d $tolX $tolY $factor $b $nx $refP
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
	    #echo $elNum
	    #echo $a $b
	    tempNum=$(( totalEle - nx + b ))
	    #echo $tempNum
        # make the klakk which is places over the middle squares
        if [ "$b" -gt 0 ] && [ "$b" -lt $nx ]
        then
            tempTransX=$(( xTrans * b ))
            python3 makeKlakk.py $l_boltekant $(( tempTransX - d_dx )) $l_SY2 $klakkRefU $klakkRefV $klakkRefW $d_dx $klakkLY $factor $d $tolBolt $depth $b $nx $refP
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
	    	python3 makeKlakk.py $l_boltekant $(( xTrans * b )) $l_SY2 $(( klakkRefU )) $klakkRefV $klakkRefW $l_boltekant $klakkLY $factor $d $tolBolt $depth 0 $nx $refP
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

# Make the outer parts/circumference of the plate
#python3 makeOuter.py $lengthX $tX1 $lengthY $tY1 $depth $factor $tolX $tolY $tolBolt $refi $d $tX2 $tY2 $yTot
#python3 merge.py total outer
#elNum=$(( elNum + 4 ))
# This will create a intermediate textfile used in the <connection> setting
python3 makeLastFile.py setsItem $nx
# Wrap it up
../../Mappe/IFEM-GPM/bin/./getGNO -v G2/total.g2 | grep "<connection" > patchFileTemp.txt
python3 qMerge.py
python3 qSort.py
python3 makeFile.py resultat.xinp G2/total.g2 setsItem.txt $N $V $elNum 3 3 8
#echo $elNum
