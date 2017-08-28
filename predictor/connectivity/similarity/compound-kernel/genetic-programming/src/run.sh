#!/bin/bash
if [ "$#" -ne 2 ]; then
  echo "[FATAL] Illegal number of parameters"
  exit 1
fi

EXE=main.py

# 0: single
# 1: parallel
if [ $1 -eq 0 ]
then
  	python $EXE
else 
	for (( i=1; i <= $2; i++ ))
	do
		echo "!!! run $i of $2 ..."
		python -m scoop -n $1 $EXE
	done
fi
