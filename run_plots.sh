VERSION=$1
MASS=$2

mkdir plots_${VERSION}/
mkdir plots_${VERSION}/vlllimits_vs_mvll
mkdir plots_${VERSION}/vlllimits_vs_ctau

#versus ctau(a)
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 10    
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 20
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 30    
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 80    
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 100
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 200   
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 300   
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 800   
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 1000
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 2000  
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 3000  
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 8000  
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 10000 
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 10    --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 30    --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 80    --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 100   --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 300   --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 800   --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 1000  --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 3000  --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 8000  --categ
python plot_VLLlimits_1D_mvll.py --unblind --version ${VERSION} --mllp ${MASS} --ctau 10000 --categ
#versus m(a)
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mllp ${MASS} --mvll 300 
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mllp ${MASS} --mvll 700 
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mllp ${MASS} --mvll 1000 
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mllp ${MASS} --mvll 300   --categ
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mllp ${MASS} --mvll 700   --categ
python plot_VLLlimits_1D_ctau.py --unblind --version ${VERSION} --mllp ${MASS} --mvll 1000  --categ