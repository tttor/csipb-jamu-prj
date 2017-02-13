import numpy as np
import urllib2 as ulib
import csv
import time

if __name__ == '__main__':
    start_time = time.time()

    outDir = "Fasta/"
    listDir = "protein.csv"
    urlDomain = "http://www.uniprot.org/uniprot/"
    protList = []
    it = 0 #flag for parsing and counter for download variable

    #Parse csv
    with open(listDir,'r') as f:
        csvContent = csv.reader(f,  delimiter=',', quotechar='\"')
        for row in csvContent:
            if (it > 0):
                protList.append(row[2])
            else:
                it = 1

    #Pull data and write file
    for i in protList:
        # print str(it)+" dari "+str(len(protList))
        connect = ulib.urlopen(urlDomain+i+".fasta")
        htmlContent = connect.read()
        with open(outDir+i+".fasta",'w') as f:
            f.write(htmlContent)
            f.close()
        it += 1
    ####Debugging section####
    print "Runtime : "+str(time.time()-start_time)
    #########################
