#!/bin/bash
ROOT=../../..
OUT_DIR=$ROOT/xprmt/similarity

SIMCOMP_DIR=$ROOT/dataset/metadata/compound/kegg/kegg_20161014/simcomp

python insert_simcomp.py $OUT_DIR $SIMCOMP_DIR
