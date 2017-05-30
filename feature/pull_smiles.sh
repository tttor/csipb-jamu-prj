# pull_smiles.sh
YAM_TYPE=nr
YAM_DIR=../dataset/connectivity/compound_vs_protein/yamanishi

LIST_FPATH=$YAM_DIR/list/compound_list_$YAM_TYPE.txt
OUT_DIR=$YAM_DIR/smiles/smiles-$YAM_TYPE

Rscript \
   pull_smiles.r \
   $LIST_FPATH \
   $OUT_DIR
