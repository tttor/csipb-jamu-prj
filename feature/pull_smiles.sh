#!/bin/bash
if [ "$#" -ne 1 ]; then
  echo "USAGE:"
  echo "bash pull_smiles.sh [yamType]"
  exit 1
fi

YAM_TYPE=$1
YAM_DIR=../dataset/connectivity/compound_vs_protein/yamanishi

LIST_FPATH=$YAM_DIR/list/compound_list_$YAM_TYPE.txt
OUT_DIR=$YAM_DIR/smiles/smiles-$YAM_TYPE
mkdir -p $OUT_DIR

Rscript \
   pull_smiles.r \
   $LIST_FPATH \
   $OUT_DIR
