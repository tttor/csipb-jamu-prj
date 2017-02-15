# Drug Predict

## Dependencies
---
### BioPython
  1. Install package : ```sudo apt-get install python-biopython```
  2. Full documentation [here](http://biopython.org/wiki/Documentation)


### Numpy
  1. Install package :
  1.Install pip : ```python -m pip install --upgrade pip```
  2.Install scoop : ```pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose```
  2. Full documentation [here](http://www.numpy.org/)

## How to Use
---
### pullUniProtFasta
  * Command: ```python pullUniProtFasta.py ```
  * Input :
    * A file named "**protein.csv**" which contain data protein dumped from DB
    * A folder named "**Fasta**" on directory
  * Output :
    * fasta files on "**Fasta**" folder with Uniprot ID as name
