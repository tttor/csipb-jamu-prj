#!/bin/bash
START_INDEX=$1
END_INDEX=$2
STEP=$3
COLUMN_STEP=$4

EXE="sim_Prot.py"

for (( i=$START_INDEX; i<$END_INDEX ;i+=$STEP))
do
    TEMP=$[$i+$STEP]
    if [ $END_INDEX -gt $TEMP ]; then
      python $EXE $i $TEMP $COLUMN_STEP
    else
      python $EXE $i $END_INDEX $COLUMN_STEP
    fi
done
