#Post-processing script for GLM simulations in the GRAPLEr
#Set up to extract multiple summary response variables from one simulation period in dataset CSV format
#Written by Cayelan Carey, last edits on 1 May 2016
#CONSOLIDATE_COMPATIBLE
#Note: need to edit the experiments directory on line 9

library(glmtools)


VarsToAnalyze = c('temp','OXY_oxy','TOT_tn','TOT_tp','PHY_TPHYS','PHY_TCHLA','PHY_CYANOPCH1','PHY_CYANONPCH2','PHY_CHLOROPCH3','PHY_DIATOMPCH4','PHY_PPR','TOT_tss') 
Depths = list(c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24), c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)) # if you want all depths, leave as NULL, otherwise, put depths that you want data for here

SimDir = paste(getwd(), 'Results', sep = "/") # from the nc file
SimFile = paste(SimDir,'output.nc',sep = "/") # from the nc file

setwd(SimDir)

myOriginalDataPC = get_var(SimFile,VarsToAnalyze[1],reference = "surface") #this is needed to figure out how long the simulation datetime vector is to initialize the temporary vectors

#time to initialize ALL the vectors!  booyah.
temp1<-rep(NA, length(myOriginalDataPC$DateTime))
temp2<-rep(NA, length(myOriginalDataPC$DateTime))
temp3<-rep(NA, length(myOriginalDataPC$DateTime))
temp4<-rep(NA, length(myOriginalDataPC$DateTime))
temp5<-rep(NA, length(myOriginalDataPC$DateTime))
temp6<-rep(NA, length(myOriginalDataPC$DateTime))
temp7<-rep(NA, length(myOriginalDataPC$DateTime))
temp8<-rep(NA, length(myOriginalDataPC$DateTime))
temp9<-rep(NA, length(myOriginalDataPC$DateTime))
temp10<-rep(NA, length(myOriginalDataPC$DateTime))
temp11<-rep(NA, length(myOriginalDataPC$DateTime))
temp12<-rep(NA, length(myOriginalDataPC$DateTime))
temp13<-rep(NA, length(myOriginalDataPC$DateTime))
temp14<-rep(NA, length(myOriginalDataPC$DateTime))
temp15<-rep(NA, length(myOriginalDataPC$DateTime))
temp16<-rep(NA, length(myOriginalDataPC$DateTime))
temp17<-rep(NA, length(myOriginalDataPC$DateTime))
temp18<-rep(NA, length(myOriginalDataPC$DateTime))
temp19<-rep(NA, length(myOriginalDataPC$DateTime))
temp20<-rep(NA, length(myOriginalDataPC$DateTime))
temp21<-rep(NA, length(myOriginalDataPC$DateTime))
temp22<-rep(NA, length(myOriginalDataPC$DateTime))
temp23<-rep(NA, length(myOriginalDataPC$DateTime))
temp24<-rep(NA, length(myOriginalDataPC$DateTime))
temp25<-rep(NA, length(myOriginalDataPC$DateTime))
temp26<-rep(NA, length(myOriginalDataPC$DateTime))
temp27<-rep(NA, length(myOriginalDataPC$DateTime))
temp28<-rep(NA, length(myOriginalDataPC$DateTime))
temp29<-rep(NA, length(myOriginalDataPC$DateTime))
temp30<-rep(NA, length(myOriginalDataPC$DateTime))
temp31<-rep(NA, length(myOriginalDataPC$DateTime))
temp32<-rep(NA, length(myOriginalDataPC$DateTime))
temp33<-rep(NA, length(myOriginalDataPC$DateTime))
temp34<-rep(NA, length(myOriginalDataPC$DateTime))
temp35<-rep(NA, length(myOriginalDataPC$DateTime))
temp36<-rep(NA, length(myOriginalDataPC$DateTime))
temp37<-rep(NA, length(myOriginalDataPC$DateTime))
temp38<-rep(NA, length(myOriginalDataPC$DateTime))
temp39<-rep(NA, length(myOriginalDataPC$DateTime))
temp40<-rep(NA, length(myOriginalDataPC$DateTime))
temp41<-rep(NA, length(myOriginalDataPC$DateTime))
temp42<-rep(NA, length(myOriginalDataPC$DateTime))
  
  # Load NETCDF file
 if(file.exists(SimFile)){
    Message = paste('Simulation successfully loaded', sep="")
    print(Message)
   for (i in 1:length(VarsToAnalyze)){
      # ExperimentPC
      VarName = VarsToAnalyze[i]
      print('==============================================')
      print(paste('Analysis of ', VarName))
      print('==============================================')
      zDepth = Depths[[i]]
      print(paste('Depth: ',zDepth))
      if (is.null(zDepth)){
        myOriginalDataPC = get_var(SimFile,VarName,reference = "surface") #CAN CHANGE THIS TO "BOTTOM"
        }else{
        myOriginalDataPC = get_var(SimFile,VarName,reference = "surface", z_out = zDepth)}
        
		if(VarName=="temp"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp1[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26]))))#pull out only the 0-24 m intervals for each timestep and take avg
				temp2[j]<-(max(na.omit(myOriginalDataPC[j,2:26])))
				temp41[j]<-(sum(na.omit(myOriginalDataPC[j,2:4])))/(3-length(which(is.na(myOriginalDataPC[j,2:26]))))#pull out only the 0-2 m interval and take avg
				temp42[j]<-(max(na.omit(myOriginalDataPC[j,2:4]))) #max observed in 0-2 m
			}
			mean_mean_temp<-mean(na.omit(temp1)) #mean temp of entire water column
			max_max_temp<-max(na.omit(temp2)) #max TN of entire water column 
			mean_surface_temp<-mean(na.omit(myOriginalDataPC$wtr_0)) #mean temp of surface 0m
			max_surface_temp<-max(na.omit(myOriginalDataPC$wtr_0)) #max temp of surface 0m
			mean_bottom_temp<-mean(na.omit(myOriginalDataPC$wtr_24)) #mean temp of bottom 24 m
			max_bottom_temp<-max(na.omit(myOriginalDataPC$wtr_24)) #max temp of bottom 24 m
			min_bottom_temp<-min(na.omit(myOriginalDataPC$wtr_24)) #min temp of bottom 24 m
			mean_0_2_temp<-mean(na.omit(temp41)) #mean temp from 0-2 m 
			max_0_2_temp<-max(na.omit(temp42)) #max temp from 0-2 m
		}
      	if(VarName=="OXY_oxy"){
			mean_bottom_oxy<-mean(na.omit(myOriginalDataPC$wtr_24))*0.032 #mean oxygen of bottom 24 m in mg/L
			min_bottom_oxy<-min(na.omit(myOriginalDataPC$wtr_24))*0.032 #min oxygen of bottom 24 m in mg/L
			hypoxic_length<-(length(which(myOriginalDataPC$wtr_24*.032<2)))# of time steps at 24 m with oxygen below 2 mg/L
	  		anoxic_length<-(length(which(myOriginalDataPC$wtr_24*.032<1)))#of time steps at 24 m with oxygen below 1 mg/L
		}
		if(VarName=="TOT_tn"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp3[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-24 m intervals for each timestep and take avg
				temp4[j]<-(max(na.omit(myOriginalDataPC[j,2:26]))) #max observed in water column
				temp5[j]<-(sum(na.omit(myOriginalDataPC[j,2:4])))/(3-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-2 m interval and take avg
				temp6[j]<-(max(na.omit(myOriginalDataPC[j,2:4]))) #max observed in 0-2 m
			}
			mean_mean_TN<-mean(na.omit(temp3))*0.014 #mean TN of entire water column in mg/L
			max_max_TN<-max(na.omit(temp4))*0.014 #max TN of entire water column	in mg/L
			mean_0_2_TN<-mean(na.omit(temp5))*0.014 #mean TN from 0-2 m in mg/L
			max_0_2_TN<-max(na.omit(temp6))*0.014 #max TN from 0-2 mg in mg/L
		}
		if(VarName=="TOT_tp"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp7[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-24 m intervals for each timestep and take avg
				temp8[j]<-(max(na.omit(myOriginalDataPC[j,2:26])))
				temp9[j]<-(sum(na.omit(myOriginalDataPC[j,2:4])))/(3-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-2 m interval and take avg
				temp10[j]<-(max(na.omit(myOriginalDataPC[j,2:4]))) #max observed in 0-2 m
			}
			mean_mean_TP<-mean(na.omit(temp7))*0.031 #mean TP of entire water column in mg/L
			max_max_TP<-max(na.omit(temp8))*0.031 #max TP of entire water column	in mg/L
			mean_0_2_TP<-mean(na.omit(temp9))*0.031 #mean TP from 0-2 m in mg/L
			max_0_2_TP<-max(na.omit(temp10))*0.031 #max TP from 0-2 mg in mg/L
		}
		if(VarName=="PHY_TPHYS"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp11[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-24 m intervals for each timestep and take avg
				temp12[j]<-(max(na.omit(myOriginalDataPC[j,2:26])))
				temp13[j]<-(sum(na.omit(myOriginalDataPC[j,2:4])))/(3-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-2 m interval and take avg
				temp14[j]<-(max(na.omit(myOriginalDataPC[j,2:4]))) #max observed in 0-2 m
			}
			mean_mean_totalphytos<-mean(na.omit(temp11)) #mean total phytos of entire water column in mmol C/m3
			max_max_totalphytos<-max(na.omit(temp12)) #max total phytos of entire water column in mmol C/m3
			mean_0_2_totalphytos<-mean(na.omit(temp13)) #mean total phytos from 0-2 m in mg/L
			max_0_2_totalphytos<-max(na.omit(temp14)) #max total phytos from 0-2 mg in mg/L
		}
		if(VarName=="PHY_TCHLA"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp15[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-24 m intervals for each timestep and take avg
				temp16[j]<-(max(na.omit(myOriginalDataPC[j,2:26])))
				temp17[j]<-(sum(na.omit(myOriginalDataPC[j,2:4])))/(3-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-2 m interval and take avg
				temp18[j]<-(max(na.omit(myOriginalDataPC[j,2:4]))) #max observed in 0-2 m

			}
			mean_mean_totalchla<-mean(na.omit(temp15)) #mean total chla of entire water column in ug/L
			max_max_totalchla<-max(na.omit(temp16)) #max total chla of entire water column in ug/L
			mean_0_2_totalchla<-mean(na.omit(temp17)) #mean total chla from 0-2 m in mg/L
			max_0_2_totalchla<-max(na.omit(temp18)) #max total chla from 0-2 mg in mg/L
		}
		if(VarName=="PHY_CYANOPCH1"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp19[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-24 m intervals for each timestep and take avg
				temp20[j]<-(max(na.omit(myOriginalDataPC[j,2:26])))
				temp21[j]<-(sum(na.omit(myOriginalDataPC[j,2:4])))/(3-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-2 m interval and take avg
				temp22[j]<-(max(na.omit(myOriginalDataPC[j,2:4]))) #max observed in 0-2 m
			}
			mean_mean_Nfixingcyanos<-mean(na.omit(temp19)) #mean Nfixingcyanos of entire water column
			max_max_Nfixingcyanos<-max(na.omit(temp20)) #max Nfixingcyanos of entire water column
			mean_0_2_Nfixingcyanos<-mean(na.omit(temp21)) #mean Nfixingcyanos from 0-2 m in mg/L
			max_0_2_Nfixingcyanos<-max(na.omit(temp22)) #max Nfixingcyanos from 0-2 mg in mg/L
		}
		if(VarName=="PHY_CYANONPCH2"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp23[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-24 m intervals for each timestep and take avg
				temp24[j]<-(max(na.omit(myOriginalDataPC[j,2:26])))
				temp25[j]<-(sum(na.omit(myOriginalDataPC[j,2:4])))/(3-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-2 m interval and take avg
				temp26[j]<-(max(na.omit(myOriginalDataPC[j,2:4]))) #max observed in 0-2 m
			}
			mean_mean_nonNfixingcyanos<-mean(na.omit(temp23)) #mean nonNfixingcyanos of entire water column
			max_max_nonNfixingcyanos<-max(na.omit(temp24)) #max nonNfixingcyanos of entire water column	
			mean_0_2_nonNfixingcyanos<-mean(na.omit(temp25)) #mean nonNfixingcyanos from 0-2 m in mg/L
			max_0_2_nonNfixingcyanos<-max(na.omit(temp26)) #max nonNfixingcyanos from 0-2 mg in mg/L
		}
      	if(VarName=="PHY_CHLOROPCH3"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp27[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-24 m intervals for each timestep and take avg
				temp28[j]<-(max(na.omit(myOriginalDataPC[j,2:26])))
				temp29[j]<-(sum(na.omit(myOriginalDataPC[j,2:4])))/(3-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-2 m interval and take avg
				temp30[j]<-(max(na.omit(myOriginalDataPC[j,2:4]))) #max observed in 0-2 m
			}
			mean_mean_chlorophytes<-mean(na.omit(temp27)) #mean chlorophytes of entire water column
			max_max_chlorophytes<-max(na.omit(temp28)) #max chlorophytes of entire water column	
			mean_0_2_chlorophytes<-mean(na.omit(temp29)) #mean chlorophytes from 0-2 m in mg/L
			max_0_2_chlorophytes<-max(na.omit(temp30)) #max chlorophytes from 0-2 mg in mg/L
		}
      if(VarName=="PHY_DIATOMPCH4"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp31[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-24 m intervals for each timestep and take avg
				temp32[j]<-(max(na.omit(myOriginalDataPC[j,2:26])))
				temp33[j]<-(sum(na.omit(myOriginalDataPC[j,2:4])))/(3-length(which(is.na(myOriginalDataPC[j,2:26]))))#pull out only the 0-2 m interval and take avg
				temp34[j]<-(max(na.omit(myOriginalDataPC[j,2:4]))) #max observed in 0-2 m
			}
			mean_mean_diatoms<-mean(na.omit(temp31)) #mean diatoms of entire water column
			max_max_diatoms<-max(na.omit(temp32)) #max diatoms of entire water column
			mean_0_2_diatoms<-mean(na.omit(temp33)) #mean diatoms from 0-2 m in mg/L
			max_0_2_diatoms<-max(na.omit(temp34)) #max diatoms from 0-2 mg in mg/L	
		}
		if(VarName=="PHY_PPR"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp35[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-24 m intervals for each timestep and take avg
				temp36[j]<-(max(na.omit(myOriginalDataPC[j,2:26])))
				temp37[j]<-(sum(na.omit(myOriginalDataPC[j,2:4])))/(3-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-2 m interval and take avg
				temp38[j]<-(max(na.omit(myOriginalDataPC[j,2:4]))) #max observed in 0-2 m
			}
			mean_mean_GPP<-mean(na.omit(temp35)) #mean gpp of entire water column
			max_max_GPP<-max(na.omit(temp36)) #max gpp of entire water column	
			mean_0_2_GPP<-mean(na.omit(temp37)) #mean GPP from 0-2 m in mg/L
			max_0_2_GPP<-max(na.omit(temp38)) #max GPP from 0-2 mg in mg/L
		}
       if(VarName=="TOT_tss"){
			for(j in 1:length(myOriginalDataPC$DateTime)){
				temp39[j]<-(sum(na.omit(myOriginalDataPC[j,2:26])))/(25-length(which(is.na(myOriginalDataPC[j,2:26])))) #pull out only the 0-24 m intervals for each timestep and take avg
				temp40[j]<-(max(na.omit(myOriginalDataPC[j,2:26])))
			}
			mean_mean_TSS<-mean(na.omit(temp39)) #mean TSS of entire water column
			max_max_TSS<-max(na.omit(temp40)) #max TSS of entire water column	
		}
    }
 
    
dataset<-data.frame(mean_mean_temp,max_max_temp,mean_surface_temp,max_surface_temp,mean_bottom_temp,max_bottom_temp,min_bottom_temp,mean_0_2_temp,max_0_2_temp,mean_bottom_oxy,min_bottom_oxy,hypoxic_length,anoxic_length,mean_mean_TN,max_max_TN,mean_0_2_TN,max_0_2_TN,mean_mean_TP,max_max_TP,mean_0_2_TP,max_0_2_TP,mean_mean_totalphytos,max_max_totalphytos,mean_0_2_totalphytos,max_0_2_totalphytos,mean_mean_totalchla,max_max_totalchla,mean_0_2_totalchla,max_0_2_totalchla,mean_mean_Nfixingcyanos,max_max_Nfixingcyanos,mean_0_2_Nfixingcyanos,max_0_2_Nfixingcyanos,mean_mean_nonNfixingcyanos,max_max_nonNfixingcyanos,mean_0_2_nonNfixingcyanos,max_0_2_nonNfixingcyanos,mean_mean_chlorophytes,max_max_chlorophytes,mean_0_2_chlorophytes,max_0_2_chlorophytes,mean_mean_diatoms,max_max_diatoms,mean_0_2_diatoms,max_0_2_diatoms,mean_mean_GPP,max_max_GPP,mean_0_2_GPP,max_0_2_GPP,mean_mean_TSS,max_max_TSS)
    
    file.remove(list.files('.'))
    }else{ Message = paste('Experiment unsuccessful', sep="") 
    print(Message)
    }#end of for loop of # of sims if there is more than one folder    

write.csv(dataset, paste0("sim_op", ".csv"),row.names = FALSE)
