#!/bin/bash
mainkeyword='diabetes mellitus'
declare -a keywords=("medicinal plant" "bioactivity" "bioassay" "extracts" "natural products")
# declare -a years=(2015 2014 2013 2012 2011 2010 2009 2008 2007 2006 2005 2004 2003 2002 2001 2000)
declare -a years=(1999 1998 1997 1996 1995 1994 1993 1992 1991 1990 1989 1988 1987 1986 1985 1984 1983 1982 1981 1980 1979 1978 1977 1976 1975 1974)
db=pubmed

out_dir=/home/tor/jamu/xprmnt/pubmed-article/05
mkdir -p $out_dir

for keyword in "${keywords[@]}"
do
	for year in "${years[@]}"
	do
		timestamp="$(date +'%Y%m%d.%H%M%S')"
		out_filepath=$out_dir/esearch.$timestamp.xml
		meta_filepath=$out_dir/esearch.$timestamp.meta

		query=(-query "$mainkeyword [TIAB] AND $keyword [TIAB] AND $year [PDAT]")

		#
		echo 'esearch for' "${query[@]}"
		esearch_tic="$(date +'%Y%m%d.%H%M%S')"

		esearch -db $db "${query[@]}" | \
		efetch -format xml > $out_filepath

		esearch_toc="$(date +'%Y%m%d.%H%M%S')"

		#
		echo $db >> $meta_filepath
		echo "${query[@]}" >> $meta_filepath
		echo $year >> $meta_filepath
		echo $keyword >> $meta_filepath
		echo $esearch_tic >> $meta_filepath
		echo $esearch_toc >> $meta_filepath
	done
done
