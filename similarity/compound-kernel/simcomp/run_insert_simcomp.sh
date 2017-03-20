#!/bin/bash
EXE=insert_simcomp.py
OUT_DIR=../../../xprmt/similarity
SIMCOMP_DIR=../../../dataset/metadata/compound/kegg/kegg_20161014/simcomp

python $EXE $OUT_DIR $SIMCOMP_DIR
