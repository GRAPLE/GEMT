#!/usr/bin/Rscript
library(rjson)
library(glmtools)
currentdir = getwd()
print(currentdir)
setwd(paste(currentdir, "../../Scripts", sep="/"))
tempRJSON = fromJSON(file = "FilterParams.json")
VarsToAnalyze = character(0)
Depths = list()
for(i in 1:length(tempRJSON))
{
  VarsToAnalyze = c(VarsToAnalyze, names(tempRJSON[i]))
  Depths = c(Depths, list(tempRJSON[[i]]$Depths))
}
setwd(paste(currentdir, "Results", sep="/"))
SimDir = paste(getwd(),"", sep="/") 
SimFile = 'output.nc' 
listOfFiles = character(0)
print(getwd())
# Load NETCDF file
if (file.exists(SimFile)){
  Message = paste('Simulation successfully loaded', sep="")
  print(Message)
  for (iV in 1:length(VarsToAnalyze))
  {
    VarName = VarsToAnalyze[iV]
   
    print('==============================================')
    print(paste('Analysis of ', VarName))
    print('==============================================')
    zDepth = Depths[[iV]]
    print(paste('Depth: ',zDepth))
    if (is.null(zDepth)){
      myOriginalDataPC = get_var(SimFile,var_name = VarName,reference = 'surface')
    } 
    else{
      myOriginalDataPC = get_var(SimFile,var_name = VarName,reference = 'surface', z_out = zDepth)
    }
    # Write output to disk
    write.csv(myOriginalDataPC,file = paste(SimDir, '/', VarName,'.csv',sep=""))
    listOfFiles <- c(listOfFiles,paste(VarName,'.csv', sep="")) 
 }
 print(listOfFiles) 
 allFiles = list.files(".") 
 print(list(setdiff(allFiles, listOfFiles))) 
 do.call(file.remove, list(setdiff(allFiles, listOfFiles))) 
}
