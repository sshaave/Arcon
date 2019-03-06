with open('hei123.txt','a') as t1:
    with open('patchFileTemp.txt','r') as t2:
        for x in t2:
            t1.write(x)
