#!/bin/bash
if [ "$#" -ne 4 ]; then
  echo "USAGE:"
  echo "bash run.sh [cloneIDFrom] [cloneIDTo] [clusterDir] [outputDir]"
  exit 1
fi

CLONEIDFROM=$1
CLONEIDTO=$2
CLUSTERDIR=$3
OUTPUTDIR=$4

CLONES=($(seq ${CLONEIDFROM} 1 ${CLONEIDTO}))
for i in ${CLONES[@]};
do
   echo '### DEVEL '$CLUSTERDIR' => '$i' TO '$CLONEIDTO' ##########################################'
   python -m scoop devel.py $i $CLUSTERDIR $OUTPUTDIR
done

