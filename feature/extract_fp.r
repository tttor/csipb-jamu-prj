# extract_fp.r
# mol = readMolFromSmi(smi, type = 'mol')[[1]]
# fp = extractDrugKRComplete(mol)

main <- function() {
   args = commandArgs(trailingOnly=TRUE)
   if (length(args)!=3) {
      message('USAGE:')
      message('Rscript extract_fp.r [yamType] [from] [to]')
      return()
   }

   library('Rcpi')
   yamType <- args[1]
   from <- as.numeric(args[2])
   to <- as.numeric(args[3])

   ydir <- '../dataset/connectivity/compound_vs_protein/yamanishi'

   message("loading comList ...")
   fname <- paste('compound_list_',yamType,'.txt',sep='')
   f <- file(file.path(ydir,'list',fname))
   comList <- readLines(f); close(f)

   sdir <- file.path( ydir,'smiles',paste('smiles',yamType,sep='-') )
   fpdir <- file.path( ydir,'fingerprint',paste('klekotaroth',yamType,sep='-'))

   for (i in from:to) {
      com <- comList[i]
      message("extract_fp... ",com," ",i,"/",to-from+1)

      sfname <- paste(com,'.smi',sep='')
      sfpath <- file.path(sdir,sfname)

      mol <- readMolFromSmi(sfpath, type = 'mol')[[1]] # assume one-liner smi files
      fp <- extractDrugKRComplete(mol)

      fname <- paste(com,'.fpkr',sep='')
      write.table(fp, file=file.path(fpdir,fname), row.names=FALSE, col.names=FALSE)
   }
}

main()
