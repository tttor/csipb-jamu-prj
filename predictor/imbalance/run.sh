#!/bin/bash
if [ "$#" -ne 2 ]; then
  echo "USAGE:"
  echo "bash run.sh [clusterDir] [nClones]"
  exit 1
fi

CLUSTERDIR=$1
NCLONES=$2

CLONES=($(seq 1 1 ${NCLONES}))
for i in ${CLONES[@]};
do
   echo '### DEVEL  '$i'/'$NCLONES' ###############################################################'
   python -m scoop devel.py $CLUSTERDIR $i
done

