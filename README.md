# combine-llp

## CMSSW+Combine Quickstart
```bash
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit

cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.2.0
scramv1 b clean; scramv1 b

cd $CMSSW_BASE/src/
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
scram b

pip install --user flake8
pip install --user --upgrade numpy
pip install --user https://github.com/jmduarte/rhalphalib/archive/coefsq_rebase.zip
pip install --user --upgrade uproot # use uproot4
```
For reference, consult
 - https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
 - https://cms-analysis.github.io/CombineHarvester/

## Checkout this repo and create datacards:
```bash
git clone https://github.com/danielguerrero/combine-llp
cd combine-llp/
```

## Get input example files (histos_cscmodel_ootime.root,histos_dtmodel_ootime.root)
They can be found here at the LPC: /uscms/home/guerrero/nobackup/Run2/VLLAnalysis/CMSSW_10_2_13/src/combine-llp/


## Run F-test, 1st vs 2nd order. Make sure the binning is compatible with input histograms in runFtest.py
For CSC,
```bash
python runFtest.py -n 7  --v1n1=0 --v1n2=1 --toys=1000 -s 1 --ifile histos_cscmodel_ootime.root
```
For DT,
```bash
python runFtest.py -n 7  --v1n1=0 --v1n2=1 --toys=1000 -s 1 --ifile histos_dtmodel_ootime.root
```

## Check fit performance in 1st order model:
```bash
combine -M FitDiagnostics FTest/cards_n1i0/VLLModel/VLLModel_combined.root --saveShapes --saveWithUncertainties --rMin -20 --rMax 20
```