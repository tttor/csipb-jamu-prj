#!/bin/sh
curr_dir="$(dirname "$0")"

src_dir=$curr_dir/src
fig_dir=$curr_dir/pics
build_dir=$curr_dir/build
out_dir=$curr_dir/out

root_tex_name=skripsi

rm -rf $build_dir/*
mkdir -p $build_dir/pics
mkdir -p $out_dir

cp -r $fig_dir/* $build_dir/pics
cp -r $src_dir/* $build_dir

pdflatex $root_tex_name.tex
bibtex $root_tex_name.aux
pdflatex $root_tex_name.tex
pdflatex $root_tex_name.tex
cp $root_tex_name.pdf $out_dir
rm -rf $build_dir/*
