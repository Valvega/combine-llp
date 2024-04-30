VERSION=$1
mkdir plots_${VERSION}/
mkdir plots_${VERSION}/vlllimits_vs_mvll
mkdir plots_${VERSION}/vlllimits_vs_ctau
#mkdir plots_${VERSION}/vlllimits_vs_mvll_ctau

#versus ctau(a)
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 10    
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 20
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 30    
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 80    
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 100
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 200   
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 300   
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 800   
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 1000
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 2000  
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 3000  
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 8000  
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 10000 
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 10    --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 30    --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 80    --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 100   --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 300   --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 800   --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 1000  --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 3000  --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 8000  --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --ctau 10000 --categ

#versus m(a)
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mvll 300 
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mvll 700 
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mvll 1000 
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mvll 300   --categ
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mvll 700   --categ
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mvll 1000  --categ

##versus m(vll), ctau
#python plot_VLLlimits_2D_mvll_ctau.py --version ${VERSION}
