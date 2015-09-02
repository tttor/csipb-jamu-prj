#!/bin/bash

# TODO use query var
# http://superuser.com/questions/360966/how-do-i-use-a-bash-variable-string-containing-quotes-in-a-command

# diabetes mellitus [TIAB] AND medicinal plant [TIAB]
# diabetes mellitus [TIAB] AND bioactivity [TIAB]
# diabetes mellitus [TIAB] AND bioassay [TIAB]
# diabetes mellitus [TIAB] AND drugs [TIAB]
# diabetes mellitus [TIAB] AND natural products [TIAB]
# diabetes mellitus [TIAB] AND extracts [TIAB]

# -query "diabetes mellitus [TIAB] AND medicinal plant[TIAB] AND 2015 [PDAT]" | \
# -query "diabetes mellitus [TIAB] AND bioactivity [TIAB] AND 2015 [PDAT]" | \
# -query "diabetes mellitus [TIAB] AND bioassay [TIAB] AND 2015 [PDAT]" | \
# -query "diabetes mellitus [TIAB] AND drugs [TIAB] AND 2015 [PDAT]" | \

timestamp="$(date +'%Y%m%d.%H%M%S')"
out_dir=/home/tor/jamu/xprmnt/abstact-pubmed/01
mkdir -p out_dir
out_filepath=$out_dir/esearch.$timestamp.xml
meta_filepath=$out_dir/esearch.$timestamp.meta

db=pubmed
query='"diabetes mellitus [TIAB] AND drugs [TIAB]"'

echo 'esearch...'
esearch_tic="$(date +'%Y%m%d.%H%M%S')"

esearch -db $db \
		-query "diabetes mellitus [TIAB] AND natural products [TIAB] AND 2015 [PDAT]" | \
efetch -format xml > $out_filepath

# mindate=2014
# maxdate=2015
# esearch -db $db \
# 		-query "diabetes mellitus [TIAB]" | \
# 		efilter -mindate $mindate -maxdate $maxdate -datetype PDAT | \
# 		efetch -format xml > \
# 		$out_filepath

esearch_toc="$(date +'%Y%m%d.%H%M%S')"

echo $db >> $meta_filepath
echo $query >> $meta_filepath
echo $mindate >> $meta_filepath
echo $maxdate >> $meta_filepath
echo $esearch_tic >> $meta_filepath
echo $esearch_toc >> $meta_filepath
