import numpy as np
import urllib2 as ulib
import csv
import time
import sys

def main():
    start_time = time.time()
    it = 0
    if len(sys.argv)!=3:
        print "Usage: python [outputDir] [protList]"
        return

    outDir = sys.argv[1]
    listDir = sys.argv[2]
    urlDomain = "http://www.uniprot.org/uniprot/"
    # protList = ["P78549"]

    with open(listDir,'r') as f:
        csvContent = csv.reader(f,  delimiter=',', quotechar='\"')
        for row in csvContent:
            if (it > 0):
                protList.append(row[2])
            else:
                it = 1

    dataList = []
    for i in protList:
        sys.stdout.write("\rPulling Data:"+str(it)+" dari "+str(len(protList)))
        sys.stdout.flush()
        connect = ulib.urlopen(urlDomain+i+".txt")
        htmlContent = connect.read()
        lines = htmlContent.split('\n')
        words = [line.split("   ") for line in lines]
        goList = []
        for word in words:
            # print word
            headLine = word[0]
            if headLine=='DR':
                contentLine = word[1].split('; ')
                if contentLine[0]=="GO":
                    goList.append(contentLine)
        dataList.append(goList)
        it += 1

    it = 1
    for i,prot in enumerate(protList):
        sys.stdout.write("\rWriting Data:"+str(it)+" dari "+str(len(protList)))
        sys.stdout.flush()
        with open(outDir+prot+".txt",'w') as f:
            f.write('GO_ID,Aspect,Name,Source,DBSource\n')
            for go in dataList[i]:
                # print go
                f.write(go[1]+',')
                if len(go[2].split(","))>1:
                    f.write(go[2].split(":")[0]+',"'+go[2].split(":")[1]+'",')
                else:
                    f.write(go[2].split(":")[0]+','+go[2].split(":")[1]+',')
                f.write(go[3].split(":")[0]+','+go[3].split(":")[1])
                f.write('\n')
        f.close()
        it += 1
    ####Debugging section####
    print "Runtime : "+str(time.time()-start_time)
    #########################

if __name__ == '__main__':
    main()
