from get_index import get_index
from hpo_similarity.hpo_similarity.test_similarity import test_similarity


def get_similarity_prot(graph,proteinPheno,proteinA,proteinB):
	
	# init_HPO()

	proteins=[proteinA,proteinB]
	total=0
	counter=0
	resnik=0
	try:
		resnik= test_similarity(graph,proteinPheno,proteins,90,"resnik")
	except:
		resnik=0
	if(resnik!=None):
		# print resnik
		return resnik
	else:
		# print 0
		return 0

def agent_score(graph,openCompound,proteinPheno,compound1,compound2):

	indexProtein1=get_index(openCompound,compound1)
	indexProtein2=get_index(openCompound,compound2)
	# print compound1+","+compound2


	count=0
	totalPhenotypeSimilarity=0
	for row in indexProtein1:
		for row2 in indexProtein2:
			totalPhenotypeSimilarity += get_similarity_prot(graph,proteinPheno,row,row2)
			count += 1
	return totalPhenotypeSimilarity/count