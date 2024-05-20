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
cd CombineHarvester
git checkout v2.0.0
scram b

pip install --user flake8
pip install --user  numpy
pip install --user https://github.com/jmduarte/rhalphalib/archive/coefsq_rebase.zip
pip install --user uproot # use uproot4
```
For reference, consult
 - https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
 - https://cms-analysis.github.io/CombineHarvester/

## Checkout this repo and create datacards:
```bash
git clone https://github.com/danielguerrero/combine-llp
cd combine-llp/
```

## Copy input example files (histos_cscmodel_ootime.root,histos_dtmodel_ootime.root)
They can be found here at the LPC: /uscms/home/guerrero/nobackup/Run2/VLLAnalysis/CMSSW_10_2_13/src/combine-llp/
```bash
cp /uscms/home/guerrero/nobackup/Run2/VLLAnalysis/CMSSW_10_2_13/src/combine-llp/histos_cscmodel_ootime.root .
cp /uscms/home/guerrero/nobackup/Run2/VLLAnalysis/CMSSW_10_2_13/src/combine-llp/histos_dtmodel_ootime.root .
```

## Run F-test, 1st vs 2nd order
For CSC,
```bash
python runFtest.py --passBinName=CSCOOT -n 9  --v1n1=0 --v1n2=1 --toys=1000 -s 1 --ifile histos_cscmodel_ootime.root
mv FTest FTest_CSC_OOT
```
For DT,
```bash
python runFtest.py --passBinName=DTOOT -n 8  --v1n1=0 --v1n2=1 --toys=1000 -s 1 --ifile histos_dtmodel_ootime.root
mv FTest FTest_DT_OOT
```

