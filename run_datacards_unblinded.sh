VERSION=$1

#masses=(300 700 1000) #gev
#ctaus=(20 30 80 100 200 300 800 1000 2000 3000 8000 10000) #mm

masses=(200 300 400 500 600 700 800) #gev
ctaus=(1 2 3 4 5 6 7 8 9 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100 150 200 250 300 800 1000 2000 3000 8000 10000) #mm

#-------UNBLINDED INT DATACARDS
for mass in ${masses[@]}
do
    for ctau in ${ctaus[@]}
    do
        #Make CSC datacards
        python create_datacard.py --inputfile inputs_${VERSION}/histos_cscmodel_sr.root --carddir cards_${mass}_${ctau} --nbins 9 --passBinName=CSCU --vll_mass $mass --llp_ctau $ctau
        cd cards_${mass}_${ctau}/VLLModel_CSCU/
        source build.sh
        cd ../../ 
        #Make DT datacards
        python create_datacard.py --inputfile inputs_${VERSION}/histos_dtmodel_sr.root  --carddir cards_${mass}_${ctau} --nbins 8 --passBinName=DTU  --vll_mass $mass --llp_ctau $ctau
        cd cards_${mass}_${ctau}/VLLModel_DTU/
        source build.sh
        cd ../../
        #Make Combined datacards
        cd cards_${mass}_${ctau}
        combineCards.py -S passCSC=VLLModel_CSCU/SRCSCU.txt failCSC=VLLModel_CSCU/fitfailCSCU.txt passDT=VLLModel_DTU/SRDTU.txt failDT=VLLModel_DTU/fitfailDTU.txt  > CSCDT_combined.txt
        text2workspace.py -D data_obs CSCDT_combined.txt 
        cd ..
    done
done
#move all datacards to datacards folder
mkdir datacards_unblinded_${VERSION}
mv cards_* datacards_unblinded_${VERSION}

##second run the limits
cd datacards_unblinded_${VERSION}
for ctau in ${ctaus[@]}
do
    for mass in ${masses[@]}
    do
        cd cards_${mass}_${ctau}
        echo " ============================================== "
        echo "... running on mVLL=$mass and ctau=$ctau        "
        echo " ============================================== "
        #Run the CSC limits
        cd VLLModel_CSCU
        combine -M AsymptoticLimits model_combined.root -n _${mass}_${ctau} 
        cd ..
        #Run the DT limits
        cd VLLModel_DTU
        combine -M AsymptoticLimits model_combined.root -n _${mass}_${ctau} 
        cd .. 
        #Run the full combination
        combine -M AsymptoticLimits CSCDT_combined.root -n _${mass}_${ctau} 
        cd ..
    done
done
cd ..
