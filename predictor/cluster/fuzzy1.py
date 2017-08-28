import os 
import sys
import yaml
import pickle
import json
import time
import shutil
import h5py 
import numpy as np
import skfuzzy as fuzz

def main():
	if len(sys.argv)!=3:
		print 'inputan salah'
		print 'python fuzzy1.py [dataset] [OutDir]'
		print 'Contoh inputan: python fuzzy1.py nr output'
		return
	elif(os.path.exists(sys.argv[2])==False):
		os.makedirs(sys.argv[2])

	dataset=sys.argv[1]
	dataset=dataset.lower()

	OutDir="Fuzzy_protein"
	OutDir=os.path.join(sys.argv[2],OutDir)
	os.makedirs(OutDir)
	# #ambil data
	print 'checking protein feature...'
	aacFpath = "../../dataset/connectivity/compound_vs_protein/yamanishi/feature/amino-acid-composition/"
	aacFpath2="amino-acid-composition-"+dataset+".h5"
	aacFpath = os.path.join(aacFpath,aacFpath2)
	status=os.path.isfile(aacFpath)
	if status==False:
		print "fitur "+dataset+" tidak ditemukan"
		return

	#pro list
	proPath="../../dataset/connectivity/compound_vs_protein/yamanishi/list/"
	proPath2="protein_list_"+dataset+".txt"
	proPath= os.path.join(proPath,proPath2)
	with open(proPath,'r') as f:
		prolist = [line.strip() for line in f] #list protein


	aacDict = {}
	with h5py.File(aacFpath, 'r') as f:
	    for pro in [str(i) for i in f.keys()]:
	        aacDict[pro] = f[pro][:]
	        # aacDict[pro] = list( fu.map(lambda x: float('%.2f'%(x)),f[pro][:]) ) # rounding

	#transformasi data
	Dataset= []
	for k,v in aacDict.iteritems():
		Dataset.append(v)
	Dataset=np.asarray(Dataset)
	Dataset=np.transpose(Dataset)

	#cari jumlah cluster terbaik
	fpcs=[]
	for center in range(3,11):	
		cntr, degree, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
		        Dataset, center, 2, error=0.005, maxiter=1000, init=None)
		fpcs.append(fpc)
	fix_center=max(fpcs)
	fix_center=fpcs.index(fix_center)+3
	
	#modeling
	print "modeling...."
	cntr, degree, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
		        Dataset, fix_center, 2, error=0.005, maxiter=1000, init=None)
	threshold=0.3
	Stat={}
	
	print "nilai fpc:",fpc
	print "jumlah center:", fix_center

	degree=np.transpose(degree)
	degreeFile=open(os.path.join(OutDir,"Protein_degree.txt"),'a')
	saveindex=[]
	for count, item in enumerate(degree):
		index=1
		temp=[]
		for x in item:
			if x>threshold:
				temp.append(index)
			index+=1
		saveindex.append(temp)
		degreeFile.write("%s\n" % item)

	#print hasil
	str_json="{"
	for i in range (len(prolist)):
		if(i!=len(prolist)-1):
			str_json= str_json+"\"" + prolist[i] + "\"" + ":" + str(saveindex[i])+","
		else:
			str_json=str_json+"\"" + prolist[i] + "\"" + ":" + str(saveindex[i]) 
	str_json+="}"
	data=json.loads(str_json)

	hasilPath='Protein_'+dataset+'_index.json'
	hasilPath=os.path.join(OutDir,hasilPath)
	with open(hasilPath, 'a') as outfile:
	    json.dump(data, outfile,indent=2,sort_keys=True)




if __name__ == "__main__":
    main()


