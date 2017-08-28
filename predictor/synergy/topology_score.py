import numpy as np
from math import exp
from get_index import get_index
import networkx as nx

def shortest_path(network, proteinA, proteinB):
	try:
		n=nx.shortest_path_length(network,proteinA,proteinB)
	except nx.NetworkXNoPath:
		n= -1
	return n

def get_index_protein_number(indexProtein,listProtein):
	counterIndex=0
	numberIndexProtein=[]
	for row in indexProtein:
		counterList=0
		for row2 in listProtein:
			if(row2==row):
				numberIndexProtein.insert(counterIndex,counterList)
			counterList=counterList+1
		counterIndex=counterIndex+1
	return numberIndexProtein

def importance_score(importanceScore,indexP):
	listIP=[]
	counter=0
	for row in indexP:
		listIP.insert(counter,importanceScore[row])
		counter=counter+1
	return listIP


def min_d(g,indexProtein1,indexProtein2):
	counterList=0
	listMinDIJ=[]
	listDIJ=[]
	counterListSearchMin=0
	for row in indexProtein1:
		for row2 in indexProtein2:
			try:
				a= shortest_path(g,row,row2)
				listDIJ.insert(counterListSearchMin,a)
				counterListSearchMin=counterListSearchMin+1
			except:
				listDIJ=listDIJ
		# print listDIJ
		dIJNumpy=np.array(listDIJ)
		dIJNumpy=dIJNumpy[dIJNumpy!=-1]
		try:
			minDIJ=dIJNumpy.min()
		except:
			minDIJ=1000
		listMinDIJ.insert(counterList,minDIJ)
		counterList=counterList+1
		counterListSearchMin=0
		listDIJ=[]
	
	return listMinDIJ


	
def measure_side(iP,minD):
	counter=0
	sigmaIP=0
	subTS=0
	for row in iP:
		sigmaIP=sigmaIP+row
		if(minD[counter]==-1):
			subTS=subTS+row*0
		else:
			subTS=subTS+row*exp(-minD[counter])
		counter=counter+1
	if(sigmaIP==0):
		return 0
	else:
		return subTS/sigmaIP

def topological_score(g,openCompound,compound1,compound2,importanceScore,listProtein):
	

	indexProtein1=get_index(openCompound,compound1)
	indexProtein2=get_index(openCompound,compound2)
	# print indexProtein1
	# print indexProtein2
	indexP1=get_index_protein_number(indexProtein1,listProtein)
	indexP2=get_index_protein_number(indexProtein2,listProtein)
	# print indexP2
	minDIJ=min_d(g,indexProtein1,indexProtein2)
	minDJI=min_d(g,indexProtein2,indexProtein1)
	# print minDJI
	iP1=importance_score(importanceScore,indexP1)
	iP2=importance_score(importanceScore,indexP2)
	# print iP2
	leftSide=measure_side(iP1,minDIJ)
	rightSide=measure_side(iP2,minDJI)
	# print rightSide
	TS=0.5*(leftSide+rightSide)
	return TS