#!/bin/bash
if [ "$#" -ne 2 ]; then
  echo "USAGE:"
  echo "bash run.sh [dataset] [outDirPrefix]"
  exit 1
fi

N_ITER=10
METHOD=dbscan
GRAPHIC=0

DATASET=$1
OUTDIR=output/$2-$DATASET
rm -rf $OUTDIR
mkdir $OUTDIR

echo '### cluster compound ####################################################'
python -m scoop cluster.py $METHOD $N_ITER $DATASET compound $OUTDIR

echo '### cluster protein #####################################################'
python -m scoop cluster.py $METHOD $N_ITER $DATASET protein $OUTDIR

echo '### cluster into neg,pos,unlabel #########################################'
python cluster2.py cal $OUTDIR $GRAPHIC
python cluster2.py sil $OUTDIR $GRAPHIC
