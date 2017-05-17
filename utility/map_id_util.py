import urllib2 as ulib
import sys

baseURL = {'kegg':"http://rest.kegg.jp/",'pubchem':"https://pubchem.ncbi.nlm.nih.gov/rest/pug/"}

def mapKEGGToUniprot(keggID):
    retDict = dict()
    retSet = set()
    startBatch = 0
    step = 100
    nQuery = len(keggID)
    while (startBatch < nQuery):
        sys.stdout.write("\r%d of %d"%(startBatch,nQuery))
        sys.stdout.flush()
        if startBatch+step < nQuery:
            lenBatch = step
        else:
            lenBatch = nQuery - startBatch
        urlTarget = baseURL['kegg']+"conv/uniprot/"
        for i in range(startBatch,startBatch+lenBatch):
            if i>startBatch:
                urlTarget += "+"
            urlTarget+=keggID[i]
        # print "Connecting",
        connection = ulib.urlopen(urlTarget)
        # print "Connection Success"
        content = connection.read()
        lines = content.split("\n")
        for line in lines:
            # print line
            word = line.split()
            if len(word) == 0:
                continue
            up = word[0]
            # print up
            retSet.add(word[1][2:])
            if up in retDict:
                retDict[up] += [word[1][2:]]
            else:
                retDict[up] = [word[1][2:]]
        startBatch += lenBatch
    return retDict,retSet

def mapUniprotToKEGG(upID):
    retDict = dict()
    retSet = set()
    startBatch = 0
    step = 100
    nQuery = len(upID)
    while (startBatch < nQuery):
        print startBatch,
        if startBatch+step < nQuery:
            lenBatch = step
        else:
            lenBatch = nQuery - startBatch
        urlTarget = baseURL['kegg']+"conv/genes/"
        for i in range(startBatch,startBatch+lenBatch):
            if i>startBatch:
                urlTarget += "+"
            urlTarget+="uniprot:"+upID[i]
        print "Connecting",
        connection = ulib.urlopen(urlTarget)
        print "Connection Success"
        content = connection.read()
        lines = content.split("\n")
        for line in lines:
            # print line
            word = line.split()
            if len(word) == 0:
                continue
            up = word[0][3:]
            # print up
            retSet.add(word[1])
            if up in retDict:
                retDict[up] += [word[1]]
            else:
                retDict[up] = [word[1]]
        startBatch += lenBatch
    return retDict,retSet

def mapPCToCAS(pcIDs):
    retDict = dict()
    startBatch = 0
    step = 10
    nQuery = len(pcIDs)
    # Make a batch in case of RTO
    while startBatch < nQuery:
        if startBatch+step < nQuery:
            lenBatch = step
        else:
            lenBatch = nQuery - startBatch

        urlTarget = baseURL['pubchem']+'compound/cid/'
        for i in range(startBatch,startBatch+lenBatch):
            urlTarget += pcIDs[i] +','
        urlTarget += "/xrefs/rn/json"

        while True:
            try:
                connection = ulib.urlopen(urlTarget)
                break
            except ulib.URLError:
                continue
        print "Connection Success"
        content = connection.read()
        jsonString = "".join(content.split())
        contentDict = json.loads(jsonString)
        for row in contentDict['InformationList']['Information']:
            if 'RN' in row:
                retDict[row['CID']] = row['RN']
        startBatch += lenBatch
    return retDict

def mapKEGGToCAS(kID):
    retDict = dict()
    retSet = set()
    step = 100
    startBatch = 0
    nQuery = len(kID)
    qPointer = -1
    while startBatch < nQuery:
        if startBatch+step < nQuery:
            lenBatch = step
        else:
            lenBatch = nQuery - startBatch
        sys.stdout.write("\rPull %d Data of %d"%(startBatch+lenBatch,nQuery))
        sys.stdout.flush()
        urlTarget = baseURL['kegg']+"get/"
        for i in range(startBatch,startBatch+lenBatch):
            if i > startBatch:
                urlTarget += "+"
            urlTarget += kID[i]

        connection = ulib.urlopen(urlTarget)
        content = connection.read()
        lines = content.split("\n")
        pullData = False
        for line in lines:
            headWord = line[:12].rstrip()
            content = line[12:].strip()
            if len(headWord)!=0:
                if headWord == "DBLINKS":
                    pullData = True
                elif headWord == "ENTRY":
                    cID = content[:6]
                else:
                    pullData = False
            if pullData:
                dbId,record = content.split(':')
                if dbId == "CAS":
                    retSet.add(record.strip())
                    retDict[cID] = record.strip()
        startBatch += lenBatch
    return retDict,retSet
