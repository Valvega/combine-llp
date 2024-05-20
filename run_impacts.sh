MASS=$1
CTAU=$2
VERSION=$3
#create directories
mkdir impacts_${VERSION}/
mkdir impacts_${VERSION}/${MASS}_${CTAU}
cd    impacts_${VERSION}/${MASS}_${CTAU}

#No signal 
combineTool.py -M Impacts -d ../../datacards_${VERSION}/cards_${MASS}_${CTAU}/CSCDT_combined.root  --doInitialFit --robustFit 1  --setParameterRanges r=0,2 -m 125 --expectSignal 0 -t -1
combineTool.py -M Impacts -d ../../datacards_${VERSION}/cards_${MASS}_${CTAU}/CSCDT_combined.root  --doFits       --robustFit 1  --setParameterRanges r=0,2 -m 125 --expectSignal 0 -t -1 --parallel 6
combineTool.py -M Impacts -d ../../datacards_${VERSION}/cards_${MASS}_${CTAU}/CSCDT_combined.root  -o impacts_${MASS}_${CTAU}_sig_inj0.json -m 125
plotImpacts.py -i impacts_${MASS}_${CTAU}_sig_inj0.json -o impacts_${MASS}_${CTAU}_sig_inj0
rm *.root

#Signal
combineTool.py -M Impacts -d ../../datacards_${VERSION}/cards_${MASS}_${CTAU}/CSCDT_combined.root  --doInitialFit --robustFit 1  --setParameterRanges r=-2,2  -m 125 --expectSignal 1 -t -1
combineTool.py -M Impacts -d ../../datacards_${VERSION}/cards_${MASS}_${CTAU}/CSCDT_combined.root  --doFits       --robustFit 1  --setParameterRanges r=-2,2  -m 125 --expectSignal 1 -t -1 --parallel 6
combineTool.py -M Impacts -d ../../datacards_${VERSION}/cards_${MASS}_${CTAU}/CSCDT_combined.root  -o impacts_${MASS}_${CTAU}_sig_inj1.json  -m 125
plotImpacts.py -i impacts_${MASS}_${CTAU}_sig_inj1.json -o impacts_${MASS}_${CTAU}_sig_inj1
rm *.root

#exit
cd ../../