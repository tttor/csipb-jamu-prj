#!/bin/bash
# TODO hide paths
. ./login.sh

if [ "$1" == "cdb" ]; then
  python create_db.py $db $user $passwd $host $port
elif [ "$1" == "ipks" ]; then
  ### insert_plant
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003/knapsack_jsp_plant_vs_compound_2016-10-04_16:34:06.468234.pkl
  python insert_plant.py $db $user $passwd $host $port $path
elif [ "$1" == "icdb" ]; then
  ### insert_compound (1)
  mode=insertComFromDrugbank
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.pkl
  exe=insert_compound.py
  python $exe $db $user $passwd $host $port $mode $outDir $path $path2
elif [ "$1" == "icks" ]; then
  ### insert_compound (2)
  mode=insertComFromKnapsack
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003/knapsack_jsp_plant_vs_compound_2016-10-04_16:34:06.468234.pkl
  exe=insert_compound.py
  python $exe $db $user $passwd $host $port $mode $outDir $path $path2
elif [ "$1" == "uckg" ]; then
  ### update_compound from kegg (3)
  mode=updateComBasedOnKegg
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/keggCom_20161010_1-100K
  path2=/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/keggdrug_data_2016-10-11_16:58:04.683546.pkl
  exe=insert_compound.py
  python $exe $db $user $passwd $host $port $mode $outDir $path $path2
elif [ "$1" == "ucsc" ]; then
  ### update compound_simcomp from kegg
  mode=updateComSimcomp
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161014/simcomp
  exe=insert_compound.py
  python $exe $db $user $passwd $host $port $mode $outDir $path
elif [ "$1" == "ipu" ]; then
  ### insert_protein
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/uniprot/uniprot_human_dat_20160928/uniprot_sprot_human_protein.pkl
  python insert_protein.py $db $user $passwd $host $port $path
elif [ "$1" == "idu" ]; then
  ### insert_disease
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/uniprot/uniprot_human_dat_20160928/uniprot_sprot_human_disease.pkl
  python insert_disease.py $db $user $passwd $host $port $path
elif [ "$1" == "ipc" ]; then
  ### insert_plant_vs_compound
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003/knapsack_jsp_plant_vs_compound_2016-10-04_16:34:06.468234.pkl
  python insert_plant_vs_compound.py $db $user $passwd $host $port $outDir $path
elif [ "$1" == "ipd" ]; then
  ### insert_protein_vs_disease
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/uniprot/uniprot_human_dat_20160928/uniprot_sprot_human.pkl
  python insert_protein_vs_disease.py $db $user $passwd $host $port $outDir $path
elif [ "$1" == "icp" ]; then
  ### insert_compound_vs_protein
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.pkl
  python insert_compound_vs_protein.py $db $user $passwd $host $port $outDir $path
else
  echo "ERROR: Unknown mode"
  exit 1
fi
