#!/bin/bash
# TODO hide paths

. ./login.sh

if [ "$1" == "cdb" ]; then
  python create_db.py $db $user $passwd $host $port
## PLANT #######################################################################
elif [ "$1" == "ipks" ]; then
  ### insert_plant
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003/knapsack_jsp_plant_vs_compound_2016-10-04_16:34:06.468234.pkl
  python insert_plant.py $db $user $passwd $host $port $path
elif [ "$1" == "upidr" ]; then
  ### update IDR plant name
  mode=updatePlantIdrName
  outDir=/home/tor/robotics/prj/csipb-jamu-prj/xprmt/insert-data-ijah
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/plant-list/latin2idr_20170118-114630.json
  python insert_plant.py $db $user $passwd $host $port $mode $outDir $path
## COMPOUND ####################################################################
elif [ "$1" == "icdb" ]; then
  ### insert_compound (1): drugbank's compound-protein connectivity
  mode=insertComFromDrugbank
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.pkl
  exe=insert_compound.py
  python $exe $db $user $passwd $host $port $mode $outDir $path $path2
elif [ "$1" == "icks" ]; then
  ### insert_compound (2): knapsack's plant-compound connectivity
  mode=insertComFromKnapsack
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003/knapsack_jsp_plant_vs_compound_2016-10-04_16:34:06.468234.pkl
  exe=insert_compound.py
  python $exe $db $user $passwd $host $port $mode $outDir $path $path2
elif [ "$1" == "uckg" ]; then
  ### update_compound from kegg (3): kegg's compound-protein connectivity
  mode=updateComBasedOnKegg
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/keggCom_20161010_1-100K
  path2=/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/keggdrug_data_2016-10-11_16:58:04.683546.pkl
  exe=insert_compound.py
  python $exe $db $user $passwd $host $port $mode $outDir $path $path2
## PROTEIN #####################################################################
elif [ "$1" == "ipu" ]; then
  ### insert_protein: Uniprot's protein-disease connectivity
  mode=insertProteinUniprot
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/uniprot/uniprot_human_dat_20160928/uniprot_sprot_human_protein.pkl
  python insert_protein.py $db $user $passwd $host $port $mode $outDir $path
elif [ "$1" == "upsw" ]; then
  ### update protein sim based on smith-waterman
  mode=updateProteinSmithWaterman
  simFpath=/home/tor/robotics/prj/csipb-jamu-prj/dataset/smithwaterman/20161230/normCombProtKernel2500_3334.csv
  metaFpath=/home/tor/robotics/prj/csipb-jamu-prj/dataset/smithwaterman/20161230/metaCombProtKernel2500_3334.txt
  python insert_protein.py $db $user $passwd $host $port $mode $outDir $simFpath $metaFpath
elif [ "$1" == "uppdb" ]; then
  mode=updateProteinPDB
  uniprot2pdbFpath=/home/tor/robotics/prj/csipb-jamu-prj/dataset/pdb/27Nov2016/uniprot2pdb.pkl
  python insert_protein.py $db $user $passwd $host $port $mode $outDir $uniprot2pdbFpath
## DISEASE #####################################################################
elif [ "$1" == "idu" ]; then
  ### insert_disease
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/uniprot/uniprot_human_dat_20160928/uniprot_sprot_human_disease.pkl
  python insert_disease.py $db $user $passwd $host $port $path
## CONNECTIVITY ################################################################
elif [ "$1" == "ipc" ]; then
  ### insert_plant_vs_compound: knapsack
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003/knapsack_jsp_plant_vs_compound_2016-10-04_16:34:06.468234.pkl
  python insert_plant_vs_compound.py $db $user $passwd $host $port $outDir $path
elif [ "$1" == "ipd" ]; then
  ### insert_protein_vs_disease: uniprot
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/uniprot/uniprot_human_dat_20160928/uniprot_sprot_human.pkl
  python insert_protein_vs_disease.py $db $user $passwd $host $port $outDir $path
elif [ "$1" == "icp" ]; then
  ### insert_compound_vs_protein: drugbank
  path=/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.pkl
  python insert_compound_vs_protein.py $db $user $passwd $host $port $outDir $path
## TEST ########################################################################
elif [ "$1" == "test" ]; then
  python postgresql_util.py $db $user $passwd $host $port
else
  echo "ERROR: Unknown mode"
  exit 1
fi
