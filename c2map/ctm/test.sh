# http://www.ncbi.nlm.nih.gov/books/NBK179288/
esearch -db pubmed -query "lycopene cyclase" | efetch -format abstract
esearch -db pubmed -query "lycopene cyclase" | efetch -format medline 

esearch -db pubmed -query "lycopene cyclase" | \
efilter -mindate 1990 -maxdate 1999 -datetype PDAT | 
efetch -format medline

esearch -db pubmed -query "lycopene cyclase" | \
efilter -mindate 1990 -maxdate 1999 -datetype PDAT | 
efetch -format docsum

esearch -db pubmed -query "lycopene cyclase" | \
efilter -mindate 1990 -maxdate 1999 -datetype PDAT | 
efetch -format xml