#db_compound (db_drug)

## Meta
- [ ] Pubchem <br />
https://pubchemblog.ncbi.nlm.nih.gov/2014/06/19/what-is-the-difference-between-a-substance-and-a-compound-in-pubchem/

- [ ] DRUGBANK <br />
http://www.drugbank.ca/drugs/DB00114 <br />
http://www.drugbank.ca/structures/structures/small_molecule_drugs/DB01628.smiles

- [ ] KEGG compound <br />
http://www.genome.jp/dbget-bin/www_bfind?compound <br />
ftp://ftp.genome.jp/pub/kegg/medicus/drug/kcf/ <br />
http://www.genome.jp/dbget-bin/www_bget?-f+k+compound+C00032 <br />
http://www.genome.jp/dbget-bin/www_bget?-f+m+compound+C00022

## Similarity
- [ ] KEGG SIMCOMP
http://www.genome.jp/tools/gn_tools_api.html <br />
http://rest.genome.jp/simcomp/C00022/knapsack/cutoff=0.1/kcfoutput=on <br />
curl -F smiles='O=C(C(=O)O)C' -F cutoff=0.6 -F limit=10 http://rest.genome.jp/simcomp/ <br />
http://rest.genome.jp/simcomp/C00022/compound/cutoff=0.000001 <br />
http://rest.genome.jp/simcomp/C00022/compound/cutoff=0.6/dnode=2/atom=2/trick=2/trickatom=0/limit=10/chiral=off

## Convertion/translation services
* http://cts.fiehnlab.ucdavis.edu/
* http://webbook.nist.gov/chemistry/cas-ser.html
* https://www.chemspider.com/InChI.asmx
* http://openbabel.org/
