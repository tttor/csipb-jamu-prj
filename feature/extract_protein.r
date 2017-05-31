# extract_protein.r

main <- function(x) {
   args = commandArgs(trailingOnly=TRUE)
   if (length(args)!=3) {
      message('USAGE:')
      message('Rscript extract_protein.r [yamType] [from] [to]')
      return()
   }

   library('Rcpi')
   yamType <- args[1]
   from <- as.numeric(args[2])
   to <- as.numeric(args[3])
   ydir <- '../dataset/connectivity/compound_vs_protein/yamanishi'

   message("loading proList ...")
   fname <- paste('protein_list_',yamType,'.txt',sep='')
   f <- file(file.path(ydir,'list',fname))
   proList <- readLines(f); close(f)

   fasdir <- file.path( ydir,'fasta' )
   odir <- file.path( ydir,'amino-acid-composition',paste('aac',yamType,sep='-'))

   for (i in from:to) {
      pro <- proList[i]
      message("extracting... ",pro," ",i,"/",to)

      pro2 <- paste(substring(pro,1,3),substring(pro,4),sep=':')
      fasfname <- paste(pro2,'.fasta',sep='')
      fasfpath <- file.path(fasdir,fasfname)

      fas <- readFASTA(fasfpath)[[1]]
      aac <- extractProtAAC(fas)

      fname <- paste(pro,'.aac',sep='')
      write.table(aac,file=file.path(odir,fname),row.names=FALSE,col.names=FALSE)
   }
}

main()
