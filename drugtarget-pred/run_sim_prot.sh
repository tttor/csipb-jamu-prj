#!/bin/bash
START_INDEX=$1
END_INDEX=$2
STEP=$3
FLAG="-m scoop"
EXE="sim_Prot.py"
for (( i=$START_INDEX; i<$END_INDEX ;i+=$STEP+1))
do
    TEMP=$[$i+$STEP]
    if [ $END_INDEX -gt $TEMP ]; then
      python $FLAG $EXE $i $TEMP
    else
      python $FLAG $EXE $i $END_INDEX
    fi
done
