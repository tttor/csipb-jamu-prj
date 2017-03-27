#!/bin/bash
ROOT=../../..
OUT_DIR=$ROOT/xprmt/similarity

SIM_FPATH=$ROOT/dataset/metadata/protein/smithwaterman/20170304/normCombProtKernel1401_3334.csv
META_FPATH=$ROOT/dataset/metadata/protein/smithwaterman/20170304/metaCombProtKernel1400_3334.csv

python insert_sw.py $OUT_DIR $SIM_FPATH $META_FPATH
