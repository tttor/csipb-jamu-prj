#!/bin/bash
# TODO hide paths

## PLANT #######################################################################
elif [ "$1" == "upidr" ]; then
  ### update IDR plant name
  mode=updatePlantIdrName
  outDir=/home/tor/robotics/prj/csipb-jamu-prj/xprmt/insert-data-ijah
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/plant-list/latin2idr_20170118-114630.json
  python insert_plant.py $db $user $passwd $host $port $mode $outDir $path
## COMPOUND ####################################################################
elif [ "$1" == "uckg" ]; then
  ### update_compound from kegg (3): kegg's compound-protein connectivity
  mode=updateComBasedOnKegg
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/keggCom_20161010_1-100K
  path2=/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/keggdrug_data_2016-10-11_16:58:04.683546.pkl
  exe=insert_compound.py
  python $exe $db $user $passwd $host $port $mode $outDir $path $path2
## PROTEIN #####################################################################
elif [ "$1" == "uppdb" ]; then
  mode=updateProteinPDB
  uniprot2pdbFpath=/home/tor/robotics/prj/csipb-jamu-prj/dataset/pdb/27Nov2016/uniprot2pdb.pkl
  python insert_protein.py $db $user $passwd $host $port $mode $outDir $uniprot2pdbFpath
