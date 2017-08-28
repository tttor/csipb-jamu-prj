# pull_smiles.r

main <- function() {
   args = commandArgs(trailingOnly=TRUE)
   if (length(args)!=2) {
      message('USAGE:')
      message('Rscript pull_smiles.r [fpath] [odir]')
      return()
   }

   library('Rcpi')

   fpath <- args[1]
   odir <- args[2]

   message("loading comList ",fpath)
   f <- file(fpath)
   coms <- readLines(f); close(f)

   message('pulling...')
   smiList <- getSmiFromKEGG(coms)
   n <- length(smiList)

   for (i in 1:n) {
      com <- coms[i]
      message("writing... ",com," ",i,"/",n)
      smi <- smiList[i]

      fname <- paste(com,'.smi',sep='')
      f <- file(file.path(odir,fname))
      writeLines(smi,f); close(f)
    }
}

main()
