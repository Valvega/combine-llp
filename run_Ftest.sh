VERSION=$1
mkdir FTest_${VERSION}

#CSC OOT model
python runFtest.py --passBinName=CSCOOT --vll_mass 300 --llp_ctau 300 -n 9  --v1n1=0 --v1n2=1 --toys=1000 -s 1  --ifile inputs_${VERSION}/histos_cscmodel_ootime.root
rm higgsCombineVLLModel_*
mv FTest FTest_CSC_OOT
mv FTest_CSC_OOT FTest_${VERSION}
#DT OOT model
python runFtest.py --passBinName=DTOOT --vll_mass 300 --llp_ctau 300 -n 8  --v1n1=0 --v1n2=1 --toys=1000 -s 1  --ifile inputs_${VERSION}/histos_dtmodel_ootime.root
rm higgsCombineVLLModel_*
mv FTest FTest_DT_OOT
mv FTest_DT_OOT FTest_${VERSION}

#CSC IT model (blinded)
python runFtest.py --passBinName=CSCINT --vll_mass 300 --llp_ctau 300 -n 5  --v1n1=0 --v1n2=1 --toys=1000 -s 1  --ifile inputs_${VERSION}/histos_cscmodel_intime.root
rm higgsCombineVLLModel_*
mv FTest FTest_CSC_INT
mv FTest_CSC_INT FTest_${VERSION}
#DT IT model  (blinded)
python runFtest.py --passBinName=DTINT --vll_mass 300 --llp_ctau 300 -n 5  --v1n1=0 --v1n2=1 --toys=1000 -s 1  --ifile inputs_${VERSION}/histos_dtmodel_intime.root
rm higgsCombineVLLModel_*
mv FTest FTest_DT_INT
mv FTest_DT_INT FTest_${VERSION}

###JUST AFTER UNBLINDING GREEN LIGHT!!!!
##CSC (unblinded) model
#python runFtest.py --passBinName=CSCU --vll_mass 300 --llp_ctau 300 -n 9  --v1n1=0 --v1n2=1 --toys=1000 -s 1  --ifile inputs_${VERSION}/histos_cscmodel_sr.root
#rm higgsCombineVLLModel_*
#mv FTest FTest_CSC_U
##DT (unblinded) model
#python runFtest.py --passBinName=DTU --vll_mass 300 --llp_ctau 300 -n 8  --v1n1=0 --v1n2=1 --toys=1000 -s 1  --ifile inputs_${VERSION}/histos_dtmodel_sr.root
#rm higgsCombineVLLModel_*
#mv FTest FTest_CSC_U