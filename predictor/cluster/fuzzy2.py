import Tkinter 
import os
import sys
import yaml
import pickle
import json
import time
import shutil
import numpy as np
from pprint import pprint
from ast import literal_eval
import itertools
import matplotlib.pyplot as plt

def main():
	if len(sys.argv)!=2:
		print 'inputan salah'
		print 'python fuzzy2.py [InDir]'
		print 'Contoh inputan: python fuzzy1.py output'
		return
	elif os.path.exists(sys.argv[1])==False:
		print "folder target tidak ditemukan"
		return
	
	InDir=os.path.join(sys.argv[1],'Fuzzy_protein')
	InDir2=os.path.join(InDir,"analisis")
	os.makedirs(InDir2)

	jenis=['e','gpcr','ic','nr']

	for item in jenis:
		proPath='Protein_'+item+'_index.json'
		proPath=os.path.join(InDir,proPath)
		status=os.path.exists(proPath)
		if status==True:
			jenis=item
			break

	#cluster protein
	with open(proPath) as data_file:    
	    data = json.load(data_file)
	ProName= data.keys() #nama
	ProCluster= data.values() #cluster

	n_cluster=max(max(ProCluster))
	clusterPro={}
	for i in range(1,n_cluster+1):
		row=[]
		for j in range(0,len(ProCluster)):
			status= i in ProCluster[j]
			if status==True:
				ProName[j]=ProName[j].encode("utf-8")
				row.append(ProName[j])
		clusterPro[i]=row

	#cluster compound
	ComPath=os.path.join(InDir,'compound_calinskiharabaz_bestlabels.json')
	if os.path.exists(ComPath)==False:
		print "label compound tidak di temukan di direktori"
		return
	with open(ComPath) as data_file:    
	    data = json.load(data_file)
	ComName= data.keys() #nama
	comCluster= data.values() #cluster

	clusterCom={}
	for i in range (-1,len(set(comCluster))+1):
		row=[]
		for j in range (0,len(comCluster)):
			if comCluster[j]==i:
				ComName[j]=ComName[j].encode("utf-8")
				row.append(ComName[j])
		clusterCom[i]=row

	#SEDERHANAKAN BINDING ROW
	pathBin="../../dataset/connectivity/compound_vs_protein/yamanishi/ground-truth/"
	pathBin2="bind_orfhsa_drug_"+jenis+".txt"
	pathBin=os.path.join(pathBin,pathBin2)
	with open(pathBin,'r') as f:
		data=[line.strip() for line in f]
	data = map(lambda x: x.split("\t"), data)

	##ganti compound
	for i in range(-1,len(clusterCom)-1):
		for j in range(0,len(data)):
			status= data[j][1] in clusterCom[i]
			if status==True:			
				data[j][1]=i
	data.sort()
	data=list(data for data,_ in itertools.groupby(data)) #remove duplicate data
	 
	##ganti protein
	datanew=[]
	for j in range (0,len(data)):
		for x in range (1,len(clusterPro)+1):
			ttemp=data[j][0].replace(":","")	
			status=ttemp in clusterPro[x]
			if status==True:
				temp=data[j]
				temp[0]=str(x)
				datanew.append(temp)
	datanew.sort()
	datanew=list(datanew for datanew,_ in itertools.groupby(datanew)) #remove duplicate data

	konektivitas = open(os.path.join(InDir2,'konektivitas.txt'), 'a')
	for item in datanew:
  		konektivitas.write("%s\n" % item)


	#UPDATE MATRIX
	#read matrix
	PathMat="../../dataset/connectivity/compound_vs_protein/yamanishi/ground-truth/"
	PathMat2="admat_dgc_"+jenis+".txt"
	PathMat=os.path.join(PathMat,PathMat2)
	with open(PathMat,'r') as f:
		data=[line.strip() for line in f]
	dataMatrix = map(lambda x: x.split("\t"), data)

	for countP, protein in enumerate(ProName):
		for x in range (1,len(clusterPro)+1): #banyaknya cluster protein
				status= protein in clusterPro[x]
				if status==True:
					clusterP=x
					break
		for countC, compound in enumerate(ComName):
			for y in range(-1,len(clusterCom)-1): #banyaknya cluster compound
				status= compound in clusterCom[y]
				if status==True:
					clusterC=y
					break
			for data in datanew:
				if clusterP==int(data[0]) and clusterC==data[1] and int(dataMatrix[countP+1][countC+1])==0:
					dataMatrix[countP+1][countC+1]='-1' #semua 0 ke update jadi -1
					break

	#PIE CHART
	Data1=0
	Data0=0
	Datamin1=0
	fig=plt.figure()
	for i in range (1,len(dataMatrix)):
		for j in range (1, len(dataMatrix[1])):
			if dataMatrix[i][j]=='1':
				Data1+=1
			elif dataMatrix[i][j]=='0':	
				Data0+=1
			else:
				Datamin1+=1
	plt.pie([Data1, Data0,Datamin1], 					#nilai
	        colors=["green","red", "blue"],				#warna
	        labels=["1", "0 credible", "0 incredible"],	#label
	        autopct='%1.1f%%')
	plt.axis('equal') #ensure pie is round
	fig.savefig(os.path.join(InDir2,"pieChart.png"))
if __name__ == "__main__":
    main()