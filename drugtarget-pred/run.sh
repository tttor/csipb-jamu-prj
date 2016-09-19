#!/bin/bash
#$ bash run.sh 4 1 nr loocv
if [ "$#" -ne 4 ]; then
  echo "[FATAL] Illegal number of parameters"
  exit 1
fi

DATASET=$3
TYPE=$4 #kfcv, loocv

EXE=main.py
HOME=/home/tor/jamu
DATASET_DIR=$HOME/dataset/yamanishi
OUT_DIR=$HOME/xprmt/drugtarget-pred/$DATASET

BIND_FPATH=$DATASET_DIR/ground-truth/bind_orfhsa_drug_$DATASET.txt
DRUG_KERNEL_FPATH=$DATASET_DIR/similarity-mat/compound/simmat_dc_$DATASET.txt
PROTEIN_KERNEL_FPATH=$DATASET_DIR/similarity-mat/protein/simmat_dg_$DATASET.txt

# 0: single
# 1: parallel
if [ $1 -eq 0 ]
then
  	python $EXE
else 
	for (( i=1; i <= $2; i++ ))
	do
		echo "!!! run $i of $2 ..."
		python -m scoop -n $1 \
		$EXE $BIND_FPATH $DRUG_KERNEL_FPATH $PROTEIN_KERNEL_FPATH \
			 $OUT_DIR $TYPE $DATASET
	done
fi
