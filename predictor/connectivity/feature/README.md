# Features and feature-extractors

## compound features
* fingerprints
  * MolPrint2D fingerprints
    * Agarwal, S. (2010)
  * OpenBabel FP2 fingerprints.
    * Agarwal, S. (2010)

## protein features
* Amino acid composition
  * Amino acid composition (AAC)
  * Dipeptide composition (DPC)
  * Tripeptide composition (TPC)
* autocorrelation
  * Normalized Moreau-Broto autocorrelation
  * Moran autocorrelation
  * Geary autocorrelation
* Composition, Transition, Distribution (CTD)
* Conjoint Triad
* Sequence-order-coupling number
* Quasi-sequence-order descriptors
* Pseudo-amino acid composition
* Amphiphilic pseudo-amino acid composition
* protein-domains via PFAM database: http://pfam.xfam.org/
  * **Punta et al. (2012)**

## pharmacological features
* interaction profiles
  * Nascimento (2016)
  * Laarhoven, T. (2013)
  * **Laarhoven, T. (2011)**

* boostrapping, features from interaction predicted by predictors
  * Yuan, Q. (2016)

## Tools
* Rcpi: R/Bioconductor package
  * http://bioconductor.org/packages/release/bioc/html/Rcpi.html
  * sudo R CMD javareconf
  * sudo apt-get install openjdk-8-jre
  * export LD_LIBRARY_PATH=/usr/lib/jvm/java-8-oracle/jre/lib/amd64/server:$LD_LIBRARY_PATH
  * `extractDrug...(mol)` works only with at least 2 lines of smiles
    * one liner .smi will produce
      * Error in get.fingerprint(molecules, type = "kr", verbose = !silent) :
      * Must supply an IAtomContainer or something coercable to it
    * the arg `mol` is Parsed Java Molecular Object
  * java -version
    * java version "1.8.0_131"
    * Java(TM) SE Runtime Environment (build 1.8.0_131-b11)
    * Java HotSpot(TM) 64-Bit Server VM (build 25.131-b11, mixed mode)
* OpenBabel
  * https://openbabel.org/docs/dev/Fingerprints/intro.html
* protr
  * https://nanx.me/protr/
* RDKit: Open-Source Cheminformatics Software
  * http://rdkit.readthedocs.io/en/latest/GettingStartedInPython.html#fingerprinting-and-molecular-similarity
  * http://rdkit.readthedocs.io/en/latest/GettingStartedInPython.html#chemical-features-and-pharmacophores
* PROFEAT (Protein Feature Server)
  * http://bidd2.nus.edu.sg/cgi-bin/prof2015/prof_home.cgi
