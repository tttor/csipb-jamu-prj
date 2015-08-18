import os
import sys
import yaml
import scipy

import util
import c2map

g_jamu_filepath = '/home/tor/jamu/xprmnt/jamu-formula/jamu001.json'
g_protein_dir = '/home/tor/jamu/xprmnt/protein-data'
g_compound_dir = '/home/tor/jamu/xprmnt/compound-data'
g_c2mapjamu_dir = '/home/tor/jamu/xprmnt/c2mapjamu'

def main(argv):
    jamu_filepath = g_jamu_filepath
    protein_dir = g_protein_dir
    compound_dir = g_compound_dir
    c2mapjamu_dir = g_c2mapjamu_dir
    
    # Load a jamu formula
    print('Loading jamu data from %s' % jamu_filepath)
    jamu = {}
    with open(jamu_filepath) as f:  
        jamu = yaml.load(f)
    print(jamu)

    # Load significant proteins
    proteins = util.load_json_from_dir(protein_dir)
    print('len(proteins)= %d' % len(proteins))

    # Load narutal compound of jamu plants
    compounds = util.load_json_from_dir(compound_dir)
    print('len(compounds)= %d' % len(compounds))    

    # Construct the c2mapjamu
    c2mapjamu = c2map.construct(proteins, compounds)
    print c2mapjamu

    # Visualize the c2mapjamu
    # Generate random features and distance matrix.
    x = scipy.rand(40)
    D = scipy.zeros([40,40])
    for i in range(40):
        for j in range(40):
            D[i,j] = abs(x[i] - x[j])
    c2map.save_mat(D, c2mapjamu_dir+'/c2mapjamu.mat.png')
    # c2map.save_mat(c2mapjamu, c2mapjamu_dir+'/c2mapjamu.mat.png')
    # c2map.save_graph(c2mapjamu, c2mapjamu_dir)

if __name__ == '__main__':
    main(sys.argv)