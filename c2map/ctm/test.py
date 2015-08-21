from Bio import Entrez

import urllib 
import urllib2
import sys

def fetchByQuery(query,days):
    Entrez.email = "xxx" # you must give NCBI an email address
    searchHandle=Entrez.esearch(db="pmc", reldate=days, term=query, usehistory="y")
    searchResults=Entrez.read(searchHandle)
    searchHandle.close()
    webEnv=searchResults["WebEnv"]
    queryKey=searchResults["QueryKey"]
    batchSize=10
    try:
        fetchHandle = Entrez.efetch(db="pmc", retmax=100, retmode="xml", webenv=webEnv, query_key=queryKey)
        data=fetchHandle.read()
        fetchHandle.close()
        return data
    except:
        return None

days=100 #looking for papers in the last 100 days
termList=["yeast","Saccharomyces"] 

query=" AND ".join(termList)
xml_data=fetchByQuery(query,days)
if xml_data==None: 
    print 80*"*"+"\n"
    print "This search returned no hits"

else:
    f=open("pmcXml.txt" ,"w")
    f.write(xml_data)
    f.close()