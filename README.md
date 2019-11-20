# ME_Calculations
Calculate the ME for processes

Calculating ME using MadGraph 

1.	Generate a standalone MadLoop library for the evaluation of one-loop matrix elements. Generate the process for the type of ME you want.
a.	./bin/mg5_aMC
b.	import model loop_sm-lepton_masses
c.	generate g g > h > l+ l- l+ l- [QCD]
d.	output ggH_4lep_0jet

2.	Now that we have the output we can go in the SubProcesses directory to find where the ME calculator is located for a set of example internal and external momenta
a.	cd SubProcesses/PV0_0_ggepemepem 
b.	make check
c.	./check
This should output the example momenta used and the corresponding ME. 

3.	Now we want to loop over the events of the tree to get the right inputs for each event!
a.	Get the four-vectors of the internal and external legs in a text file in the same format as the output of the example four-vectors above
b.	Write a simple text file called PS.input (or edit the one that exists in the same directory) with the 4-vectors of a random event in your tree (Make sure all calculations are for the partonic rest frame)
i.	First define TLorentz vectors for your 4 final state leptons by using lepton pt, eta, phi and m
ii.	Add these to get your higgs and boost to the Higgs CM and then get lepton px, py, pz and E for the text file
iii.	Get your gluons by setting px, py as 0 and pz and E as half the higgs mass (Make sure one gluon pz is -ve while other is positive)
c.	The order of the fourvectors matters so the info about 2 gluons is the first 2 lines and then the leptons (When jets are involved is gluons, jet and then leptons)
d.	Now use make check and ./check to see if everything works!
e.	The ME is also stored in a results.dat file 
More info here: https://cp3.irmp.ucl.ac.be/projects/madgraph/wiki/MadLoopStandaloneLibrary 
The file check_sa.f has the Fortran code that does this calculation. We need to edit this code so it would read our momenta as input arguments

 
4.	Editing the fortran code to read specific input files and output the results with certain file name
Add the following lines under CHARACTER*120 BUFF(NEXTERNAL) in the LOCAL 
CHARACTER*80 ARGIN
CHARACTER*80 ARGOUT
The following lines under CALL PRINTOUT()
CALL GETARG(1,ARGIN)
And change PS.input to ARGIN in the line 

OPEN(967, FILE=ARGIN, ERR=976, STATUS='OLD',
The following lines on line ~ 299  and change results.dat to ARGOUT 
CALL GETARG(2,ARGOUT)
OPEN(69, FILE=ARGOUT, ERR=976, ACTION='WRITE')

5.	Now you can write a Python script that loops over a tree
a.	For each event it writes a file with the fourvectors
b.	Goes to the required directory and gives this file and a corresponding output file to check 
c.	Calculates the ME 
d.	Reads the ME from the results and stores it in a tree as a new variable
e.	See attached python script I

6.	Submitting this code as a batch job
a.	Make sure that all input and results files are written in the scratch area!!!
b.	Have the python code loop over as many events as you want in a single job and take in as an argument a “job number” for example, for a tree with 12000 event, job #1 does events 1-249, job #2 does events 250-499 and so on. You now need to submit 48 jobs to complete the entire tree
c.	Write another python code that writes a bash script with the right environment variables that submits 48 jobs. See attached python script II 

7.	Run the jobs, and merge all the output trees to get one minitree with the required MEs 
/home/net3/skrishna/Magic/ggH_4lep_sbi_1jet/SubProcesses/PV0_0_1_gg_epemepemg
