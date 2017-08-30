# skenario implemen ke ijah
import os
import sys

import networkx as nx
import numpy as np
import psycopg2
import pickle
import yaml

from function import *
from hpo_similarity.hpo_similarity.ontology import Ontology
from hpo_similarity.hpo_similarity.check_proband_terms import check_terms_in_graph
from hpo_similarity.hpo_similarity.test_similarity import test_similarity
from topology_score import *
from agent_score import *

with open('config_database.json','r') as f:
	dcfg = yaml.load(f)


def main():
	#start connect database

	conn = psycopg2.connect(database=dcfg['database'], user=dcfg['user'], password=dcfg['password'], host=dcfg['host'], port=dcfg['port'])
	cursor = conn.cursor()

	#end connect database


	# start input argumen
	inputCompoundID1 = sys.argv[1]
	inputCompoundID2 = sys.argv[2]
	inputDiseaseID = sys.argv[3]
	# end input argumen



	# start initialize agent score

	fp=open("hpo_similarity/hpo_similarity/data/hp.obo")
	ontology=Ontology(fp)
	graph=ontology.get_graph()
	alt = ontology.get_alt_ids()
	obsolete = ontology.get_obsolete_ids()
	obs=list(obsolete)

	cursor.execute("SELECT c.com_id,p.pro_uniprot_abbrv FROM compound_vs_protein cp inner join compound c on cp.com_id=c.com_id inner join protein p on cp.pro_id=p.pro_id where c.com_id='%s' or c.com_id='%s'"%(inputCompoundID1,inputCompoundID2))
	openCompound=cursor.fetchall()

	with open('ppi.pickle', 'rb') as handle:
	    loadPpi = pickle.load(handle)

	proteinPheno={}

	pp=[]
	with open('proteinphenotype.pickle', 'rb') as handle:
	    loadPhenotype = pickle.load(handle)

	for row in openCompound:
		for row2 in loadPhenotype:
			if(row[1]==row2[0]):
				pp.insert(0,row2)
	for row in pp:
		if (row[1] in proteinPheno):
			proteinPheno[row[0]].append(row[1])
		else:
			proteinPheno[row[0]]=[row[1]]

	for prots in proteinPheno:
	    terms = proteinPheno[prots]
	    terms = [alt[term]
	             if term in alt else term for term in terms]
	    terms1 = [term for term in terms if term not in obs]
	    proteinPheno[prots] = terms1
	graph.tally_hpo_terms(proteinPheno)
	check_terms_in_graph(graph, proteinPheno)

	# end initialize agent score

	g=nx.Graph()

	cursor.execute("SELECT dis_id,pro_id from protein_vs_disease pd where pd.dis_id='%s'"%(inputDiseaseID))

	# start count topology score
	listProteinIdIjah=[]
	pro_id=cursor.fetchall()
	for row2 in pro_id:
		listProteinIdIjah.insert(0,row2[1])

	proteinUniprotAbbrv=[]
	listCompoundIdIjah=[]

	for i in range(len(listProteinIdIjah)):
		#get protein uniprot abbrv

		cursor.execute("SELECT pro_uniprot_abbrv from protein where pro_id='%s'"%(listProteinIdIjah[i]))
		getProteinUniprotAbbrv=cursor.fetchall()
		for row2 in getProteinUniprotAbbrv:
			proteinUniprotAbbrv.insert(0,row2)

		#get protein vs compound
		cursor.execute("SELECT com_id from compound_vs_protein where pro_id='%s'"%(listProteinIdIjah[i]))
		getListCompoundId=cursor.fetchall()
		for row2 in getListCompoundId:
			listCompoundIdIjah.insert(0,row2)

	for i in range(len(proteinUniprotAbbrv)):
		for row in loadPpi:
			if(row[1]=='%s'%proteinUniprotAbbrv[i]):
				g.add_edge(row[1],row[2])

	closeness =closeness_centrality(g)
	listProtein=closeness.keys()
	closenessValues=closeness.values()

	degree =degree_centrality(g)
	degreeValues=degree.values()

	betweenness =betweenness_centrality(g)
	betweennessValues=betweenness.values()

	importanceScore=np.array([closenessValues,betweennessValues,degreeValues])
	importanceScore=importanceScore.mean(0)
	total=np.array([listProtein,closenessValues,betweennessValues,degreeValues,importanceScore])

	# end calculate feature for topological score


	#open compound protein target
	cursor.execute("SELECT c.com_id,p.pro_uniprot_abbrv FROM compound_vs_protein cp inner join compound c on cp.com_id=c.com_id inner join protein p on cp.pro_id=p.pro_id where c.com_id='%s'"%(inputCompoundID1))
	openCompound1=cursor.fetchall()
	listProteinSenyawa1=[]
	for row in openCompound1:
		listProteinSenyawa1.insert(0,row[1])
	intersectProteinSenyawa1=list(set(listProteinSenyawa1)&set(listProtein))

	cursor.execute("SELECT c.com_id,p.pro_uniprot_abbrv FROM compound_vs_protein cp inner join compound c on cp.com_id=c.com_id inner join protein p on cp.pro_id=p.pro_id where c.com_id='%s'"%(inputCompoundID2))
	openCompound2=cursor.fetchall()
	listProteinSenyawa2=[]
	for row in openCompound2:
		listProteinSenyawa2.insert(0,row[1])
	intersectProteinSenyawa2=list(set(listProteinSenyawa2)&set(listProtein))

	print "DiseaseID,Compound1,Compound2,Topology Score,Agent Score,Synergy Score"

	if(intersectProteinSenyawa1==[] or intersectProteinSenyawa2==[]):
		try:	
			AS=agent_score(graph,openCompound,proteinPheno,"%s"%inputCompoundID1,"%s"%inputCompoundID2)
		except:
			AS=-1
		print "%s"%inputDiseaseID+","+"%s"%inputCompoundID1+","+"%s"%inputCompoundID2+",-1"+","+"%s"%AS+","+"-1"
	else:
		cursor.execute("SELECT c.com_id,p.pro_uniprot_abbrv FROM compound_vs_protein cp inner join compound c on cp.com_id=c.com_id inner join protein p on cp.pro_id=p.pro_id where c.com_id='%s' or c.com_id='%s'"%(inputCompoundID1,inputCompoundID2))
		openCompound=cursor.fetchall()
		# start calculate topology and agent score
		try:
			TS=topological_score(g,openCompound,"%s"%inputCompoundID1,"%s"%inputCompoundID2,importanceScore,listProtein)
		except:
			TS=-1
		try:	
			AS=agent_score(graph,openCompound,proteinPheno,"%s"%inputCompoundID1,"%s"%inputCompoundID2)
		except:
			AS=-1
		if(TS==-1 or AS==-1):
			print "%s"%inputDiseaseID+","+"%s"%inputCompoundID1+","+"%s"%inputCompoundID2+","+"%s"%TS+","+"%s"%AS+","+"-1"
		else:
			SS=AS*TS
			print "%s"%inputDiseaseID+","+"%s"%inputCompoundID1+","+"%s"%inputCompoundID2+","+"%s"%TS+","+"%s"%AS+","+"%s"%SS


if __name__=='__main__':
	main()