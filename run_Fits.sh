VERSION=$1
mkdir postfit_${VERSION}

#postfit OOT pol0
combine -M FitDiagnostics FTest_${VERSION}/FTest_CSC_OOT/cards_n1i0/VLLModel_CSCOOT/VLLModel_combined.root  --redefineSignalPOIs r --setParameterRanges r=-2,2 --forceRecreateNLL --saveOverallShapes --saveShapes --saveWithUncertainties -n _csc_oot_pol0
combine -M FitDiagnostics FTest_${VERSION}/FTest_DT_OOT/cards_n1i0/VLLModel_DTOOT/VLLModel_combined.root   --redefineSignalPOIs r --setParameterRanges r=-2,2 --forceRecreateNLL --saveOverallShapes --saveShapes --saveWithUncertainties -n _dt_oot_pol0
rm higgsCombine_*
mv fitDiagnostics_* postfit_${VERSION}

#postfit INT pol0
combine -M FitDiagnostics FTest_${VERSION}/FTest_CSC_INT/cards_n1i0/VLLModel_CSCINT/VLLModel_combined.root    --redefineSignalPOIs r --setParameterRanges r=-2,2 --forceRecreateNLL --saveOverallShapes --saveShapes --saveWithUncertainties -n _csc_int_pol0
combine -M FitDiagnostics FTest_${VERSION}/FTest_DT_INT/cards_n1i0/VLLModel_DTINT/VLLModel_combined.root     --redefineSignalPOIs r --setParameterRanges r=-2,2 --forceRecreateNLL --saveOverallShapes --saveShapes --saveWithUncertainties -n _dt_int_pol0
rm higgsCombine_*
mv fitDiagnostics_* postfit_${VERSION}