#!/bin/bash
if [ "$#" -ne 1 ]; then
  echo "[FATAL] Illegal number of parameters"
  exit 1
fi

EXE=main.py

# 0: single
# 1: parallel
if [ $1 -eq 0 ]
then
  	python $EXE
elif [ $1 -eq 1 ]
then
	python -m scoop $EXE
	#python -m scoop --hostfile hosts $EXE  
else
  	echo "[FATAL] Unknown argument."
  	exit 1
fi
