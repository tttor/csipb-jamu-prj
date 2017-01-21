# Drug Predict

## Dependencies
---
### BioPython
  1. Install package : ```sudo apt-get install python-biopython```
  2. Full documentation [here](http://biopython.org/wiki/Documentation)

### Scoop
  1. Install package :
  1.Install pip : ```sudo apt-get install python-dev python-pip```
  2.Install scoop : ```pip install scoop```
  2. Full documentation [here](http://scoop.readthedocs.io/en/0.7/usage.html)


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

### Sim_Prot
  * Command : ```python -m scoop Sim_Prot.py rowStartIndex rowEndIndex colStartIndex colEndIndex```

  * Input :
    * A file named "**protein.csv**" which contain data protein dumped from DB
    * A folder named "**hasil**" on directory
    * A folder called "**Fasta**" which contain list of fasta file with Uniprot id as name
    * rowStartIndex : i-th row from protein.csv as **first row** of the similarity matrices
    * rowEndIndex : i-th row from protein.csv as **last row** of the similarity matrices
    * colStartIndex : i-th row from protein.csv as **first column** of the similarity matrices
    * colEndIndex : i-th row from protein.csv as **last column** of the similarity matrices

  * Output :
    * MetaProtKernel.txt : a text file which contain a list of Uniprot id column and row
    * NormProtKernel.txt : a text file which contain the normalized value of smith-waterman scoring
    * RealProtKernel.txt : a text file which contain the real value of smith waterman-scoring
