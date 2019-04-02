import sys
if sys.argv[2] == 'true':
    with open('G2/'+sys.argv[1]+'.g2','w') as i1:
        with open('G2/1Test.g2','r') as i2: i1.write(i2.read()+'\n')
        with open('G2/2Test.g2','r') as i3: i1.write(i3.read()+'\n')
        with open('G2/3Test.g2','r') as i4: i1.write(i4.read()+'\n')
        with open('G2/4Test.g2','r') as i5: i1.write(i5.read()+'\n')
        #with open('G2/elongatedSq.g2','r') as i6: i1.write(i6.read())
elif sys.argv[2] == 'middleSquares':
    with open('G2/'+sys.argv[1]+'.g2','a') as i1:
        with open('G2/elongSq.g2','r') as i2: i1.write(i2.read())
elif sys.argv[2] == 'multi':
    with open('G2/'+sys.argv[1]+'.g2','a') as i1:
        with open('G2/litenMulti.g2','r') as i2: i1.write(i2.read())
elif sys.argv[2] == 'outer':
    with open('G2/'+sys.argv[1]+'.g2','a') as i1:
        with open('G2/firstX.g2','r') as i2: i1.write(i2.read()+'\n')
        with open('G2/firstY.g2','r') as i3: i1.write(i3.read()+'\n')
        with open('G2/secondX.g2','r') as i4: i1.write(i4.read()+'\n')
        with open('G2/secondY.g2','r') as i5: i1.write(i5.read()+'\n')
elif sys.argv[2] == 'klakk':
    with open('G2/'+sys.argv[1]+'.g2','a') as i1:
        with open('G2/klakk.g2','r') as i2: i1.write(i2.read())
elif sys.argv[2] == 'claw':
    with open('G2/'+sys.argv[1]+'.g2','a') as i1:
        with open('G2/claw1.g2','r') as i2: i1.write(i2.read()+'\n')
        with open('G2/claw2.g2','r') as i3: i1.write(i3.read()+'\n')
        with open('G2/claw3.g2','r') as i4: i1.write(i4.read()+'\n')
        with open('G2/claw4.g2','r') as i5: i1.write(i5.read())
else:
    with open('G2/'+sys.argv[1]+'.g2','a') as i1:
        with open('G2/1Test.g2','r') as i2: i1.write(i2.read()+'\n')
        with open('G2/2Test.g2','r') as i3: i1.write(i3.read()+'\n')
        with open('G2/3Test.g2','r') as i4: i1.write(i4.read()+'\n')
        with open('G2/4Test.g2','r') as i5: i1.write(i5.read())
