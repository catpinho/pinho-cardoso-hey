##This R script will take a number of genpop formatted files (for adegenet) and run the dapc algorithm automatically in all of them, with the number of pcs selected using xvalDapc
## it was initially intended for bootstraps but it can simply perform the method on any large number of files
## sometimes there are convergence issues and adegenet raises warnings. In this case a file is saved with the warnings so that you can adjust the number of iterations and repeat the analyses
## The script needs to be in the same folder of the files you want to analyse which also corresponds to the working directory of R.

library(adegenet)
fc<-function(file){
	if (grepl(".gen",file)==TRUE){
		a<-read.genepop(file)
		grp<-find.clusters(a,max.n.clust=40,n.start=50,n.iter=1e5,n.pca=800,choose.n.clust=FALSE,criterion="min")
		data2<-na.replace(a,method="mean")
		xval<-xvalDapc(data2$tab,grp$grp,n.pca.max=800,training.set=0.9, result="groupMean",center=TRUE,scale=FALSE, n.pca=seq(25,by=25,to=800), n.rep=25, xval.plot=TRUE)
		dapc<-dapc(a,grp$grp,n.pca=as.integer(xval[6]),n.da=20)
		write.table(dapc$posterior,paste(file,".out",sep=""))
	}
}

saveAllWarnings <- function(f,expr, logFile="warning_log_1e5.R") {
    withCallingHandlers(expr, 
        warning=function(w) {
            cat(paste(f,conditionMessage(w),sep="\t"), "\n",  file=logFile, append=TRUE)
        })
}
b<-list.files()
for (f in b){
saveAllWarnings(f,fc(f))
}