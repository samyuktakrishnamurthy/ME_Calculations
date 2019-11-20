export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh
export LCGENV_PATH=/cvmfs/sft.cern.ch/lcg/releases
/cvmfs/sft.cern.ch/lcg/releases/lcgenv/latest/lcgenv -p LCG_85swan2 --ignore Grid x86_64-slc6-gcc49-opt root_numpy > lcgenv.sh
echo 'export PATH=$HOME/.local/bin:$PATH' >> lcgenv.sh
export LD_LIBRARY_PATH="/home/net3/skrishna/HEPTools/lib/:${LD_LIBRARY_PATH}"
source lcgenv.sh
asetup 21.2,AthAnalysis,latest,slc6

cd /home/net3/skrishna/

python Inc_ME_ggHZZ_Honly.py 695
