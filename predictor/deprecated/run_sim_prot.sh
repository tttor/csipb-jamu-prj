#!/bin/bash
START_INDEX=$1
END_INDEX=$2
STEP=$3
COLUMN_STEP=$4

FLAG="-m scoop"
EXE="Sim_Prot.py"

for (( i=$START_INDEX; i<$END_INDEX ;i+=$STEP))
do
    TEMP=$[$i+$STEP]
    if [ $END_INDEX -gt $TEMP ]; then
      python $FLAG $EXE $i $TEMP $COLUMN_STEP
    else
      python $FLAG $EXE $i $END_INDEX $COLUMN_STEP
    fi
done
