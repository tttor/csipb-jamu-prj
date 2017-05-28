#!/bin/bash
if [ "$#" -ne 3 ]; then
  echo "USAGE:"
  echo "bash run.sh [clusterDir] [cloneIDFrom] [cloneIDTo]"
  exit 1
fi

CLUSTERDIR=$1
CLONEIDFROM=$2
CLONEIDTO=$3

CLONES=($(seq ${CLONEIDFROM} 1 ${CLONEIDTO}))
for i in ${CLONES[@]};
do
   echo '### DEVEL '$CLUSTERDIR' => '$i' TO '$CLONEIDTO' ##########################################'
   python -m scoop devel.py $CLUSTERDIR $i
done

