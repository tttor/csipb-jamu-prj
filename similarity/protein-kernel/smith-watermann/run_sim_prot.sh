#!/bin/bash
if [ "$#" -ne 5 ]; then
  echo "[FATAL] Illegal number of parameters"
  exit 1
fi

START_INDEX=$1
END_INDEX=$2
STEP=$3
COLUMN_STEP=$4
POOL=$5
EXE="sim_Prot.py"

for (( i=$START_INDEX; i<$END_INDEX ;i+=$STEP))
do
    TEMP=$[$i+$STEP]
    if [ $END_INDEX -gt $TEMP ]; then
      python $EXE $i $TEMP $COLUMN_STEP $POOL
    else
      python $EXE $i $END_INDEX $COLUMN_STEP $POOL
    fi
done
