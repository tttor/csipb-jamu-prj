# skenario implemen ke ijah
import os
import sys

import networkx as nx
import numpy as np
np.set_printoptions(threshold='nan')
import psycopg2
import matplotlib.pyplot as plt

from function import *
from hpo_similarity.hpo_similarity.ontology import Ontology
from hpo_similarity.hpo_similarity.check_proband_terms import check_terms_in_graph
from hpo_similarity.hpo_similarity.test_similarity import test_similarity
from topology_score import *
from agent_score import *

inputCompoundID1 = sys.argv[1]
inputCompoundID2 = sys.argv[2]
inputDiseaseID = sys.argv[3]

database = psycopg2.connect(host='localhost', port='5432', dbname='ijah', user='postgres', password='postgres')
cursor = database.cursor()


# start initialize agent count agent score

fp=open("hpo_similarity/hpo_similarity/data/hp.obo")
ontology=Ontology(fp)
graph=ontology.get_graph()
alt = ontology.get_alt_ids()
obsolete = ontology.get_obsolete_ids()
obs=list(obsolete)

cursor.execute("SELECT c.com_id,p.pro_uniprot_abbrv FROM compound_vs_protein cp inner join compound c on cp.com_id=c.com_id inner join protein p on cp.pro_id=p.pro_id where c.com_id='%s' or c.com_id='%s'"%(inputCompoundID1,inputCompoundID2))
openCompound=cursor.fetchall()

proteinPheno={}
cursor.execute("SELECT protein,hpo_id from protein_phenotype2")
pp=cursor.fetchall()
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




cursor.execute("SELECT count(dis_id) from disease where dis_id='%s'"%(inputDiseaseID))
totalDisease=cursor.fetchall()
counter=1

#contoh DIS00003796
cursor.execute("SELECT distinct dis_id from disease where dis_id='%s' order by dis_id"%(inputDiseaseID))
dis_id=cursor.fetchall()

for disid in dis_id:
	g=nx.Graph()

	cursor.execute("SELECT dis_id,pro_id from protein_vs_disease pd where pd.dis_id=%s",(disid))
	
	# start count topology score
	listProteinIdIjah=[]
	pro_id=cursor.fetchall()
	for row2 in pro_id:
		# print row2[0]+row2[1]
		listProteinIdIjah.insert(0,row2[1])

	# print listProteinIdIjah

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

	# get compound name
	# compoundName=[]
	# for i in range(len(listCompoundIdIjah)):
	# 	cursor.execute("SELECT com_pubchem_name from compound where com_id=%s",(listCompoundIdIjah[i]))
	# 	getCompoundName=cursor.fetchall()
	# 	for row2 in getCompoundName:
	# 		compoundName.insert(0,"%s"%row2)
	# print compoundName

	for i in range(len(proteinUniprotAbbrv)):
		cursor.execute("SELECT protein1,protein2 from ppi_ijah_2 where protein1=%s and score>908",(proteinUniprotAbbrv[i]))
		ppi=cursor.fetchall()
		for row2 in ppi:
			g.add_edge(row2[0],"%s"%row2[1])

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
	
	# end count topological score

	# print total.transpose()
	'''
	draw graph
	nx.draw(g)

	# plt.show()

	plt.savefig('name.png')
	os.system('eog name.png &')
	'''

	# start count topology and agent score

	#open compound protein target
	cursor.execute("SELECT c.com_id,p.pro_uniprot_abbrv FROM compound_vs_protein cp inner join compound c on cp.com_id=c.com_id inner join protein p on cp.pro_id=p.pro_id where c.com_id='%s' or c.com_id='%s'"%(inputCompoundID1,inputCompoundID2))
	openCompound=cursor.fetchall()
	

	# for row in range(len(listCompoundIdIjah)):
	# 	row2=row
	# 	for row2 in range(row+1,len(listCompoundIdIjah)):
	# 		TS=topological_score(g,openCompound,"%s"%listCompoundIdIjah[row],"%s"%listCompoundIdIjah[row2],importanceScore,listProtein)
	# 		AS=agent_score(graph,openCompound,proteinPheno,"%s"%listCompoundIdIjah[row],"%s"%listCompoundIdIjah[row2])
	# 		SS=AS*TS
	# 		print "%s"%disid+","+"%s"%listCompoundIdIjah[row]+","+"%s"%listCompoundIdIjah[row2]+","+"%s"%TS+","+"%s"%AS+",%s"%SS

	TS=topological_score(g,openCompound,"%s"%inputCompoundID1,"%s"%inputCompoundID2,importanceScore,listProtein)
	AS=agent_score(graph,openCompound,proteinPheno,"%s"%inputCompoundID1,"%s"%inputCompoundID2)
	SS=AS*TS
	print "%s"%disid+","+"%s"%inputCompoundID1+","+"%s"%inputCompoundID2+","+",%s"%SS

	counter=counter+1

	# nx.draw(g)

	# # plt.show()

	# plt.savefig('name.png')
	# os.system('eog name.png &')

	# g=g.clear()
	# g.clear()

	# print g.nodes()



