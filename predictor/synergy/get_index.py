def get_index(compound,compoundSearch):
	indexProtein=[]
	listIndexCounterProtein=0
	for compo in compound:
		if (compo[0]==compoundSearch):
			indexProtein.insert(listIndexCounterProtein,compo[1])
			listIndexCounterProtein=listIndexCounterProtein+1

	return indexProtein