with open('tempFiles/updatePatchFile.txt','a') as t1:
    with open('tempFiles/patchFileTemp.txt','r') as t2:
        for x in t2:
            t1.write(x)
