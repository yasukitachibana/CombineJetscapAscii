import os
import sys
import pathlib
import re
import numpy as np

def Combine(args):

#    h_switch = True
#    p_switch = False
#    s_switch = True

    h_switch = False
    p_switch = True
    s_switch = False

    
    print('\n### Filename Starting with '+args.head_hadron)
    cwd = os.getcwd()
    print('### Directory '+cwd+'\n')
    
    filename = args.head_hadron+'*'+args.suffix+'{}.*'

    import glob
    list = glob.glob(filename.format(0))

    n_list = len(list)
    i_list = 0
    
    for seq in list:
        
        i_list = i_list +1

        print(i_list,'/',n_list)

        this_seq_filename = seq.replace(args.suffix+'0.',args.suffix+'{}.')
        combined_filename = seq.replace(args.suffix+'0.','.')

        this_seq_parton_filename = this_seq_filename.replace(args.head_hadron,args.head_parton)
        combined_parton_filename = combined_filename.replace(args.head_hadron,args.head_parton)

        this_seq_sigma_filename = this_seq_filename.replace(args.head_hadron,args.head_sigma)
        combined_sigma_filename = combined_filename.replace(args.head_hadron,args.head_sigma)
        

        ########### HADRON ###########
        if h_switch:
            if os.path.isfile(combined_filename):
                os.remove(combined_filename)        
            pathlib.Path(combined_filename).touch()
            print(combined_filename)
        ########### PARTON ###########
        if p_switch:
            if os.path.isfile(combined_parton_filename):
                os.remove(combined_parton_filename)
            pathlib.Path(combined_parton_filename).touch()
            print(combined_parton_filename)
        ########### SIGMA ###########
        if s_switch:
            if os.path.isfile(combined_sigma_filename):
                os.remove(combined_sigma_filename)
            pathlib.Path(combined_sigma_filename).touch()
            print(combined_sigma_filename)
        
        event = 0
        event_parton = 0
        
        n_run = 0;
        sum = 0.0;
        err2 = 0.0;
        
        for i in range(args.file_num):

            ########### HADRON ###########
            if h_switch:
                file_list = this_seq_filename.format(i)

                if not os.path.isfile(file_list):
                    break
                    #print(file_list)
                f = open(file_list)
                lines = f.readlines()
                f.close()
            
                for i_line in range(len(lines)):
                    if '#' in lines[i_line]:
                        event = event+1
                        lines[i_line] = re.sub('Event.*ID','Event'+str(event)+'ID',lines[i_line])

                file = open(combined_filename, 'a')
                file.writelines(lines)

            ########### PARTON ###########
            if p_switch:
                file_list = this_seq_parton_filename.format(i)

                if not os.path.isfile(file_list):
                    break
                    #print(file_list)
                f = open(file_list)
                lines = f.readlines()
                f.close()
            
                for i_line in range(len(lines)):
                    if '#' in lines[i_line]:
                        event_parton = event+1
                        lines[i_line] = re.sub('Event.*ID','Event'+str(event_parton)+'ID',lines[i_line])

                file = open(combined_parton_filename, 'a')
                file.writelines(lines)

            ########### SIGMA ###########
            if s_switch:
                file_sigma = this_seq_sigma_filename.format(i)
                if not os.path.isfile(file_sigma):
                    break
                #print(file_sigma)
                sigma = np.loadtxt(file_sigma)
                n_run = n_run + 1
                sum = sum + sigma[0]
                err2 = err2 + sigma[1]*sigma[1]

        if s_switch:            
            sigma_avr = np.array([sum/n_run, np.sqrt(err2)/n_run]).T
            np.savetxt(combined_sigma_filename, [sigma_avr])
        

def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, default="./")
    parser.add_argument("--suffix", type=str, default="_Run")
    parser.add_argument("--file_num", type=int, default=100)
    parser.add_argument("--head_hadron", type=str, default="JetscapeHadronList")
    parser.add_argument("--head_parton", type=str, default="JetscapePartonList")
    parser.add_argument("--head_sigma", type=str, default="SigmaHard")
    args = parser.parse_args()
    
    home = os.getcwd()
    os.chdir(args.dir)
    Combine(args)
    os.chdir(home)



if __name__ == '__main__':
    main()
