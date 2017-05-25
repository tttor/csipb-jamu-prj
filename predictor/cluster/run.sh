#!/bin/bash
if [ "$#" -ne 3 ]; then
  echo "USAGE:"
  echo "bash run.sh [nIter] [dataset] [outDirPrefix]"
  exit 1
fi

N_ITER=$1
METHOD=dbscan

DATASET=$2
OUTDIR=output/$3-$DATASET
rm -rf $OUTDIR
mkdir $OUTDIR

echo '### cluster compound ####################################################'
python -m scoop cluster.py $METHOD $N_ITER $DATASET compound $OUTDIR

echo '### cluster protein #####################################################'
python -m scoop cluster.py $METHOD $N_ITER $DATASET protein $OUTDIR

echo '### cluster into neg,pos,unlabel #########################################'
python cluster2.py cal $OUTDIR
python cluster2.py sil $OUTDIR
