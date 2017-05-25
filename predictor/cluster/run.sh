#!/bin/bash
if [ "$#" -ne 2 ]; then
  echo "USAGE:"
  echo "bash run.sh [dataset] [outDirPrefix]"
  exit 1
fi

N_ITER=10
METHOD=dbscan
DATASET=$1

OUTDIR=output/$2-$DATASET
rm -rf $OUTDIR
mkdir $OUTDIR

echo '### cluster compound ####################################################'
python -m scoop cluster.py $METHOD $N_ITER $DATASET compound $OUTDIR

echo '### cluster protein #####################################################'
python -m scoop cluster.py $METHOD $N_ITER $DATASET protein $OUTDIR
