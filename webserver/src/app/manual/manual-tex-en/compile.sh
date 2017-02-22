#!/bin/sh
root_tex_name=main

rm *.log *.aux *.blg *.bbl
pdflatex $root_tex_name.tex
bibtex $root_tex_name.aux
pdflatex $root_tex_name.tex
pdflatex $root_tex_name.tex

manual=../../../../api/ijah_webserver_manual.pdf
mv main.pdf $manual

