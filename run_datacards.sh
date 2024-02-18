VERSION=$1
masses=(300 700 1000)
ctaus=(10 20 30 80 100 200 300 800 1000 2000 3000 8000 10000)

#first just make the combine datacards and workspaces
for mass in ${masses[@]}
do
    for ctau in ${ctaus[@]}
    do
        #Make CSC datacards
        python create_datacard.py --inputfile inputs_${VERSION}/histos_cscmodel.root --carddir cards_${mass}_${ctau} --nbins 9 --passBinName=CSCB --vll_mass $mass --llp_ctau $ctau
        cd cards_${mass}_${ctau}/VLLModel_CSCB/
        source build.sh
        cd ../../ 
        #Make DT datacards
        python create_datacard.py --inputfile inputs_${VERSION}/histos_dtmodel.root  --carddir cards_${mass}_${ctau} --nbins 8 --passBinName=DTB  --vll_mass $mass --llp_ctau $ctau
        cd cards_${mass}_${ctau}/VLLModel_DTB/
        source build.sh
        cd ../../
        #Make Combined datacards
        cd cards_${mass}_${ctau}
        combineCards.py passCSC=VLLModel_CSCB/SRCSCB.txt failCSC=VLLModel_CSCB/fitfailCSCB.txt passDT=VLLModel_DTB/SRDTB.txt failDT=VLLModel_DTB/fitfailDTB.txt > CSCDT_combined.txt
        text2workspace.py CSCDT_combined.txt
        cd ..
    done
done

#move all datacards to datacards folder
rm -r datacards_${VERSION}
mkdir datacards_${VERSION}
mv cards_* datacards_${VERSION}

#second run the limits
cd datacards_${VERSION}
for ctau in ${ctaus[@]}
do
    for mass in ${masses[@]}
    do
        cd cards_${mass}_${ctau}
        echo " ============================================== "
        echo "... running on mVLL=$mass and ctau=$ctau        "
        echo " ============================================== "
        #Run the CSC limits
        cd VLLModel_CSCB
        combine -M AsymptoticLimits --run blind model_combined.root --redefineSignalPOIs r -n _${mass}_${ctau} --rMax 400
        cd ..
        #Run the DT limits
        cd VLLModel_DTB
        combine -M AsymptoticLimits --run blind model_combined.root --redefineSignalPOIs r -n _${mass}_${ctau} --rMax 400
        cd .. 
        #Run the full combination
        combine -M AsymptoticLimits --run blind CSCDT_combined.root --redefineSignalPOIs r -n _${mass}_${ctau} --rMax 400
        cd ..
    done
done
cd ..
