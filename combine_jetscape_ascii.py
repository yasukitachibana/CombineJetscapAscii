import os
import sys
import pathlib
import re
import numpy as np

def Combine(args):
    
    print('\n### Filename Starting with '+args.head_hadronlist)
    cwd = os.getcwd()
    print('### Directory '+cwd+'\n')
    
    filename = args.head_hadronlist+'*'+args.suffix+'{}.*'

    import glob
    list = glob.glob(filename.format(0))
    
    for seq in list:
        
        this_seq_filename = seq.replace(args.suffix+'0.',args.suffix+'{}.')
        combined_filename = seq.replace(args.suffix+'0.','.')

        this_seq_sigma_filename = this_seq_filename.replace(args.head_hadronlist,args.head_sigma)
        combined_sigma_filename = combined_filename.replace(args.head_hadronlist,args.head_sigma)
        
        if os.path.isfile(combined_filename):
            os.remove(combined_filename)
        if os.path.isfile(combined_sigma_filename):
            os.remove(combined_sigma_filename)
            
        print(combined_filename)
        print(combined_sigma_filename)
        
        pathlib.Path(combined_filename).touch()
        pathlib.Path(combined_sigma_filename).touch()
        
        event = 0
        
        n_run = 0;
        sum = 0.0;
        err2 = 0.0;
        
        for i in range(args.filenumber_max):
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

            file_sigma = this_seq_sigma_filename.format(i)
            if not os.path.isfile(file_sigma):
                break
            #print(file_sigma)
            sigma = np.loadtxt(file_sigma)
            n_run = n_run + 1
            sum = sum + sigma[0]
            err2 = err2 + sigma[1]*sigma[1]
            
        sigma_avr = np.array([sum/n_run, np.sqrt(err2)/n_run]).T
        np.savetxt(combined_sigma_filename, [sigma_avr])
        

def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target_directory", type=str, default="./")
    parser.add_argument("--suffix", type=str, default="_Run")
    parser.add_argument("--filenumber_max", type=int, default=100)
    parser.add_argument("--head_hadronlist", type=str, default="JetscapeHadronList")
    parser.add_argument("--head_sigma", type=str, default="SigmaHard")
    args = parser.parse_args()
    
    home = os.getcwd()
    os.chdir(args.target_directory)
    Combine(args)
    os.chdir(home)



if __name__ == '__main__':
    main()
