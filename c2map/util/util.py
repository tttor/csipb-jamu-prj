import os
import glob
import yaml

def load_json_from_dir(dirpath):
    out_list = []
    for filepath in glob.glob(os.path.join(dirpath, '*.json')):
        print('opening: %s' % filepath)
    
        i = {}    
        with open(filepath) as f:  
            i = yaml.load(f)
        out_list.append(i)

    return out_list

def gen_protein_meta():
	pass



