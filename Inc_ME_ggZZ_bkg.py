#This code reads a minitree and does the following
#calculate the FV
#Puts the FV through MadGraph
#Calculates the ME for the ???
#creates a new minitree with these new variables

import subprocess
import numpy as np
from ROOT import *
import os
import shutil, sys
#Minitree we are reading from

# defining th paths for different directories
home2 = "/scratch/skrishna"
scratchArea = "/scratch/"

#os.mkdir("skrishna")
os.chdir(scratchArea)

#home = "/gpfs3/umass/HZZ/MG5_aMC_v3_0_0/"

path_0jet_ggHZZ = "./Tar_ggH_4lep_0jet/SubProcesses/PV0_0_1_gg_h_epemepem/"
path_1jet_ggHZZ = "./Tar_ggH_4lep_1jet/SubProcesses/PV0_0_1_gg_gh_gepemepem/"
path_0jet_ggZZ = "./Tar_ggnoH_4lep_0jet/SubProcesses/PV0_0_1_gg_epemepem/"
path_1jet_ggZZ = "./Tar_ggnoH_4lep_1jet/SubProcesses/PV0_0_1_gg_gepemepem"

#Defining the TLorentzVectors
lep1Z1 = TLorentzVector()
lep2Z1 = TLorentzVector() 
lep1Z2 = TLorentzVector()
lep2Z2 = TLorentzVector()
jet1 = TLorentzVector() 
jet1_corr = TLorentzVector() 
gluon1 = TLorentzVector()
gluon2 = TLorentzVector()
lep2Z2_corr = TLorentzVector()

#module that calculates the ME
def Calculate_ME(i):
    #define home
    TarArea = scratchArea+"tmp_ggZZ_16e_"+str(i)

    myfile = TFile('/home/net3/skrishna/minitrees/v_19/mc16e/mc16_13TeV.345709.Sherpa_222_NNPDF30NNLO_ggllllNoHiggs_130M4l.root')
    #get the minitree from the TFile and loop over the entries
    mytree = myfile.Get('tree_incl_all')
    entries = mytree.GetEntriesFast()

    #output Tree with new branches
    test = "mc16e_ggZZ_130_bkg_" +str(i)+ ".root"
    f = TFile(test,'RECREATE')

    #creating a new directory in the scratch area and moving there
    if (os.path.isdir("tmp_ggZZ_16e_"+str(i))==True):
        file_copy = "/scratch/tmp_ggZZ_16e_"+str(i)+"/"
        print ("here")
        subprocess.call("ls")
        subprocess.call("pwd")
        shutil.rmtree(file_copy)
#        sys.exit()
       #shutil.rmtree("tmp_ggHZZ_"+str(i))
        
    os.mkdir("tmp_ggZZ_16e_"+str(i))
    os.chdir("tmp_ggZZ_16e_"+str(i))

    #defining i/o files for check_sa.f to read and write to prevent overwriting
    ps_input =  TarArea + "input_ggZZ_bkg_"+str(i)+".input"
    results =  TarArea + "output_ggZZ_bkg_"+str(i)+".dat"

    #scping the MG code over to scratch and untaring the files
    subprocess.call(["scp", "abc-at13:/gpfs3/umass/HZZ/MG5_aMC_v3_0_0/ggH_4lep_0jet.tar.gz","./"])
    #subprocess.call(["scp", "abc-at13:/gpfs3/umass/HZZ/MG5_aMC_v3_0_0/ggH_4lep_1j.tar.gz","./"])
    subprocess.call(["scp", "abc-at13:/gpfs3/umass/HZZ/MG5_aMC_v3_0_0/ggnoH_4lep_0j.tar.gz","./"])
    #subprocess.call(["scp", "abc-at13:/gpfs3/umass/HZZ/MG5_aMC_v3_0_0/ggnoH_4lep_1j.tar.gz","./"])

    subprocess.call(["tar","-xzf","ggH_4lep_0jet.tar.gz"])
    #subprocess.call(["tar","-xzf","ggH_4lep_1j.tar.gz"])
    subprocess.call(["tar","-xzf","ggnoH_4lep_0j.tar.gz"])
    #subprocess.call(["tar","-xzf","ggnoH_4lep_1j.tar.gz"])


    #defining all the required variables for new branches
    ggHZZ_ME_0j = np.array([0.])
    ggHZZ_ME_1j = np.array([0.])
    ggZZ_ME_0j = np.array([0.])
    ggZZ_ME_1j = np.array([0.])

    #cloning the old tree to get a new tree
    newTree = mytree.CloneTree(0)
    #adding all the new ME branches
    newTree.Branch("ggHZZ_ME_0j", ggHZZ_ME_0j, 'ggHZZ_ME_0j/D')
    newTree.Branch("ggHZZ_ME_1j", ggHZZ_ME_1j, 'ggHZZ_ME_1j/D')
    newTree.Branch("ggZZ_ME_0j", ggZZ_ME_0j, 'ggZZ_ME_0j/D')
    newTree.Branch("ggZZ_ME_1j", ggZZ_ME_1j, 'ggZZ_ME_1j/D')
   
    #Loop over entries in the tree
    i_events = i*228
    for jentry in range(i_events, i_events + 228):
        ientry = mytree.LoadTree(jentry)
        if ientry < 0:
            break
        nb = mytree.GetEntry(jentry)
        if nb<=0:
            continue 

        #Prepare 4-vectors for the two leptons of the first Z
        lep1Z1.SetPtEtaPhiM(mytree.lepton_pt[0], mytree.lepton_eta[0], mytree.lepton_phi[0], 0)
        lep2Z1.SetPtEtaPhiM(mytree.lepton_pt[1], mytree.lepton_eta[1], mytree.lepton_phi[1], 0)
        #Prepare 4-vectors for the two leptons of the second Z
        lep1Z2.SetPtEtaPhiM(mytree.lepton_pt[2], mytree.lepton_eta[2],mytree.lepton_phi[2], 0)
        lep2Z2.SetPtEtaPhiM(mytree.lepton_pt[3], mytree.lepton_eta[3],mytree.lepton_phi[3], 0)
        
        ggHZZ_ME_0j_value = 0.1
        ggHZZ_ME_1j_value = 99
        ggZZ_ME_0j_value = 0.1
        ggZZ_ME_1j_value = 99

        ########################
        #       0 JET ME       #
        ########################
        
        if mytree.n_jets >=0: #this passes all evnents

            #Reconstructing 0 jet higgs
            vecZ1= (lep1Z1 + lep2Z1)
            vecZ2= (lep1Z2 + lep2Z2)
            vecHiggs = vecZ1 + vecZ2
            #Boosting the leptons to the CM frame
            lep1Z1.Boost(-vecHiggs.BoostVector())
            lep1Z2.Boost(-vecHiggs.BoostVector())
            lep2Z1.Boost(-vecHiggs.BoostVector())
            lep2Z2.Boost(-vecHiggs.BoostVector())
            #Setting the gluons with pz as half the energy of the higgs
            gluon1.SetPxPyPzE(0,0,vecHiggs.M()/2, vecHiggs.M()/2)
            gluon2.SetPxPyPzE(0,0,-vecHiggs.M()/2, vecHiggs.M()/2)

            #Correcting the fourth lepton fourvectors to impose energy-momentum conservation
            lep2Z2_corr_px = - (lep1Z1.Px()+lep2Z1.Px()+lep1Z2.Px())
            lep2Z2_corr_py = - (lep1Z1.Py()+lep2Z1.Py()+lep1Z2.Py())
            lep2Z2_corr_pz = - (lep1Z1.Pz()+lep2Z1.Pz()+lep1Z2.Pz())
            lep2Z2_corr_e = np.sqrt(lep2Z2_corr_px**2+lep2Z2_corr_py**2+lep2Z2_corr_pz**2)
            lep2Z2_corr.SetPxPyPzE(lep2Z2_corr_px, lep2Z2_corr_py, lep2Z2_corr_pz, lep2Z2_corr_e);
          
            #File to which the FV is written that is the input for the check_sa.f
            #Now written in the /scratch area!!
            FV_file = open(ps_input, "w")

            #Output file for the Fourvectors
            if lep1Z1.Px()==lep1Z1.Px():
                FV_file.write('%f %f %f %f \n' %(gluon1.E(),gluon1.Px(), gluon1.Py(), gluon1.Pz()))
                FV_file.write('%f %f %f %f \n' %(gluon2.E(),gluon2.Px(), gluon2.Py(), gluon2.Pz()))           
                FV_file.write('%f %f %f %f \n' %(lep1Z1.E(),lep1Z1.Px(), lep1Z1.Py(), lep1Z1.Pz()))
                FV_file.write('%f %f %f %f \n' %(lep2Z1.E(),lep2Z1.Px(), lep2Z1.Py(), lep2Z1.Pz()))
                FV_file.write('%f %f %f %f \n' %(lep1Z2.E(),lep1Z2.Px(), lep1Z2.Py(), lep1Z2.Pz())) 
                FV_file.write('%f %f %f %f \n' %(lep2Z2.E(),lep2Z2.Px(), lep2Z2.Py(), lep2Z2.Pz()))
            FV_file.close()     
           
  
            ########################
            #     ggHZZ ME-0j      #
            ########################     
            os.chdir(TarArea)
            #going to the right directory
            os.chdir(path_0jet_ggHZZ)   

            #compile and calculate the ME
            subprocess.call(["make","clean"])
            subprocess.call(["make","check"])
            subprocess.call(["./check",ps_input,results])
            #Read the ME from the results file
            file = open(results, "r")                
            outputLines = file.readlines()
            #getting the right line from the results file, and reading the ME value, 
            imp_line = outputLines[8]
            ME_list1 = imp_line.split('         ')                
            #print type(ME_list[1])
            ggHZZ_ME_0j_value = float(ME_list1[1])
            print(ME_list1[1])
            os.remove(results)
            #going back to home directory to start another calculation
            os.chdir(TarArea)
           
            ########################
            #     ggZZ ME-0j       #
            ########################
            
            os.chdir(path_0jet_ggZZ)
            #compile and calculate the ME
            subprocess.call(["make","clean"])
            subprocess.call(["make","check"])
            subprocess.call(["./check",ps_input,results])
            #Read the ME from the results file
            file = open(results, "r")
            outputLines = file.readlines()
            #getting the right line from the results file, and reading the ME value,
            imp_line = outputLines[8]
            ME_list2 = imp_line.split('         ')
            #Print and check ME filling
            ggZZ_ME_0j_value = float(ME_list2[1]) 
            print(ME_list2[1])
            os.remove(ps_input)
            os.remove(results)
               
            if mytree.n_jets >=0 :
                ggHZZ_ME_1j[0]=99.
                ggZZ_ME_1j[0]=99.
                ggHZZ_ME_0j[0] = ggHZZ_ME_0j_value
                ggZZ_ME_0j[0] = ggZZ_ME_0j_value
                newTree.Fill()
               
            os.chdir(TarArea)                   
            """
            
            ########################
            #       1 JET ME       #
            ########################
            #picking one jet events here
            if mytree.n_jets >0 :
                jet1.SetPtEtaPhiM(mytree.jet_pt[0], mytree.jet_eta[0], mytree.jet_phi[0], mytree.jet_m[0])
                #getting the Higgs Fv taking jets into account
                vecZ1= (lep1Z1 + lep2Z1)
                vecZ2= (lep1Z2 + lep2Z2)
                vecHiggs = vecZ1 + vecZ2 + jet1
                #Boosting the leptons to the CM frame   
                lep1Z1.Boost(-vecHiggs.BoostVector())
                lep1Z2.Boost(-vecHiggs.BoostVector())
                lep2Z1.Boost(-vecHiggs.BoostVector())
                lep2Z2.Boost(-vecHiggs.BoostVector())
                jet1.Boost(-vecHiggs.BoostVector())
                #Setting the gluons with pz as half the energy of the higgs
                gluon1.SetPxPyPzE(0,0,vecHiggs.M()/2, vecHiggs.M()/2)
                gluon2.SetPxPyPzE(0,0,-vecHiggs.M()/2, vecHiggs.M()/2)        
                #Correcting the jet fourvectors to impose energy-momentum conservation
                jet1_corr_px = - (lep1Z1.Px()+lep2Z1.Px()+lep1Z2.Px()+lep2Z2.Px())
                jet1_corr_py = - (lep1Z1.Py()+lep2Z1.Py()+lep1Z2.Py()+lep2Z2.Py())
                jet1_corr_pz = - (lep1Z1.Pz()+lep2Z1.Pz()+lep1Z2.Pz()+lep2Z2.Pz())
                jet1_corr_e = np.sqrt(jet1_corr_px**2+jet1_corr_py**2+ jet1_corr_pz**2)
                jet1_corr.SetPxPyPzE(jet1_corr_px, jet1_corr_py, jet1_corr_pz, jet1_corr_e)
                
                
                #################################################
                #Additional Energy momentum conservation check!!#
                #################################################
                
                net_energy = gluon1.E()+ gluon2.E() - lep1Z1.E() - lep2Z1.E() - lep1Z2.E() - lep2Z2.E() - jet1_corr.E()
                print(net_energy)
                #File to which the FV is written that is the input for the check_sa.f
                #again, this is now in /scratch area!!
                FV_file = open(ps_input, "w")
                if (net_energy < 1):
                    
                    #writing the fourvectors
                    if lep1Z1.Px()==lep1Z1.Px():
                        FV_file.write('%f %f %f %f \n' %(gluon1.E(),gluon1.Px(), gluon1.Py(), gluon1.Pz()))
                        FV_file.write('%f %f %f %f \n' %(gluon2.E(),gluon2.Px(), gluon2.Py(), gluon2.Pz()))
                        FV_file.write('%f %f %f %f \n' %(jet1_corr.E(), jet1_corr.Px(), jet1_corr.Py() ,jet1_corr.Pz()))
                        FV_file.write('%f %f %f %f \n' %(lep1Z1.E(),lep1Z1.Px(), lep1Z1.Py(), lep1Z1.Pz()))
                        FV_file.write('%f %f %f %f \n' %(lep2Z1.E(),lep2Z1.Px(), lep2Z1.Py(), lep2Z1.Pz()))
                        FV_file.write('%f %f %f %f \n' %(lep1Z2.E(),lep1Z2.Px(), lep1Z2.Py(), lep1Z2.Pz()))
                        FV_file.write('%f %f %f %f \n' %(lep2Z2.E(),lep2Z2.Px(), lep2Z2.Py(), lep2Z2.Pz()))
                    FV_file.close()
                        
                    ########################
                    #     ggHZZ ME-1j      #
                    ########################
            
                    #going to the right directory
                    os.chdir(path_1jet_ggHZZ)
                    #compile and calculate the ME
                    subprocess.call(["make", "clean"])
                    subprocess.call(["make","check"])
                    subprocess.call(["./check",ps_input,results])
                    #Read the ME from the results file
                    file = open(results, "r")
                    outputLines = file.readlines()
                    #getting the right line from the results file, and reading the ME value,
                    imp_line = outputLines[9]
                    ME_list3 = imp_line.split('         ')
                    
                    os.remove(results)  
                    os.chdir(TarArea)
     
                    ########################
                    #     ggZZ ME-1j       #
                    ########################
            
                    #going to the right directory
                    os.chdir(path_1jet_ggZZ)
                    #compile and calculate the ME
                    subprocess.call(["make", "clean"])
                    subprocess.call(["make","check"])
                    subprocess.call(["./check",ps_input,results])
                    #Read the ME from the results file
                    file = open(results, "r")
                    outputLines = file.readlines()
                    #getting the right line from the results file, and reading the ME value,
                    imp_line = outputLines[9]
                    ME_list4 = imp_line.split('         ')
                    #print type(ME_list[1])
                    os.remove(ps_input)
                    os.remove(results)
                    
                print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDd")
                ggZZ_ME_1j_value = float(ME_list4[1])                
                print(ME_list4[1])
                ggHZZ_ME_1j_value = float(ME_list3[1])  
                print(ME_list3[1])
                #Fill the tree with ME            
                ggHZZ_ME_0j[0] = ggHZZ_ME_0j_value
                ggZZ_ME_0j[0] = ggZZ_ME_0j_value
                ggHZZ_ME_1j[0] = ggHZZ_ME_1j_value
                ggZZ_ME_1j[0] = ggZZ_ME_1j_value
 
                """
   
        print("######################################################################################################################################")
        print(newTree.ggHZZ_ME_0j)
        print(newTree.ggZZ_ME_0j)
        print(newTree.ggHZZ_ME_1j)
        print(newTree.ggZZ_ME_1j)
 
        os.chdir(TarArea)
   
    os.chdir(scratchArea)

    f.Write()
    f.Close()

    file_1 = "tmp_ggZZ_16e_"+str(i)
    subprocess.call(["rm","-rf",file_1])
    #os.remove(file_1)

    minitree = "./"+test
#subprocess.call("pwd")
#subprocess.call("ls")

    #copy the tree back to gpfs
    subprocess.call(["scp", minitree ,"abc-at13:/gpfs3/umass/HZZ/MG5_aMC_v3_0_0/test_copied_trees/bkg/mc16e/"])
    subprocess.call(["rm","-rf",test])
        
  
if __name__ == "__main__":
    import sys
    Calculate_ME(int(sys.argv[1]))

