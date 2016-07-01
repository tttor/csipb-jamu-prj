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
else 
	python -m scoop -n $1 $EXE
fi
