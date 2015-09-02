'''
Make data into json-format, from simple listing
'''
import sys
import json

def get_sym2desc_map():
	filepath = '/home/tor/jamu/xprmnt/protein-data/list/protein_sym2desc_map.csv'

	sym2desc = [line.rstrip('\n') for line in open(filepath)]

	sym2desc_map = {}
	for i in sym2desc:
		e = i.split(',')
		e = [i.lower() for i in e]
		sym2desc_map[e[0]] = e[1].strip(' "')

	return sym2desc_map

def make_protein_json():
	list_filepath = '/home/tor/jamu/xprmnt/protein-data/list/protein.list'
	out_dir = '/home/tor/jamu/xprmnt/protein-data/ori'

	proteins = [line.rstrip('\n') for line in open(list_filepath)]
	sym2desc_map = get_sym2desc_map()

	idx = 0
	for p in proteins:
		idx = idx + 1
		id_str = 'pro' + format(idx, '03d')
		e = p.split(',')
		e = [i.lower() for i in e]
		d = {'id': id_str, 'symbol': e[0], 'description': sym2desc_map[e[0]], \
			 'bc': e[1], 'cc': e[2]}

		with open(out_dir+'/'+id_str+'.json','w') as f:
 			json.dump(d, f)

def make_compound_json():
	list_filepath = '/home/tor/jamu/xprmnt/compound-data/list/compound.list'
	out_dir = '/home/tor/jamu/xprmnt/compound-data/ori'

	compounds = [line.rstrip('\n') for line in open(list_filepath)]

	idx = 0
	for c in compounds:
		idx = idx + 1
		id_str = 'com' + format(idx, '03d')
		e = c.split(',')
		e = [i.strip('"').lower() for i in e]
		d = {'id': id_str, 'name': e[1], \
			 'containing_plant': e[0], 'cid': e[2]}

		with open(out_dir+'/'+id_str+'.json','w') as f:
 			json.dump(d, f)

def main(argv):
	if argv[1] == 'com':
		make_compound_json()
	elif argv[1] == 'pro':
		make_protein_json()
	else:
		print 'ERR; unknown'
	
if __name__ == '__main__':
	main(sys.argv)
