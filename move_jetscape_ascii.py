import os
import sys
import pathlib
import re
import numpy as np
import glob
import shutil
import generate_qsub_command as qcom

def Move(args):
    
    home = os.getcwd()
    os.chdir(args.target_directory)
    
    print('\n### Filename Starting with '+args.head_hadronlist)
    cwd = os.getcwd()
    print('### From Directory '+cwd+' to '+args.destination+'\n')
    

    filename = args.head_hadronlist+'*.*'
    excl_filename = args.head_hadronlist+'*'+args.suffix+'*.*'
    
    list = set(glob.glob(filename)) - set(glob.glob(excl_filename))
    print(list)
    i_file=0
    n_file=len(list)
    for file in list:
        i_file = i_file + 1
        print(i_file,'/',N_file)

        #shutil.copyfile(file,os.path.join(args.destination,file))
        command = '"cp '+os.path.join(cwd,file)+' '+os.path.join(args.destination,file)+'"'
        master_command = os.path.join(home,'JobMaster') + ' "" ' + command
        qsub_command = qcom.GenerateQsubCommand(string(i_file),master_command)
        print('Submission: ')
        print(qsub_command)
        os.system(qsub_command)
        print('###')

    filename = args.head_sigma+'*.*'
    excl_filename = args.head_sigma+'*'+args.suffix+'*.*'

    list = set(glob.glob(filename)) - set(glob.glob(excl_filename))
    print(list)

    for file in list:
        command = '"cp '+os.path.join(cwd,file)+' '+os.path.join(args.destination,file)+'"'
        master_command = os.path.join(home,'JobMaster') + ' "" ' + command
        qsub_command = qcom.GenerateQsubCommand(string(i_file),master_command)
        print('Submission: ')
        print(qsub_command)
        os.system(qsub_command)
        print('###')

    
    os.chdir(home)

def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target_directory", type=str, default="./")
    parser.add_argument("--destination", type=str, default="./test")
    parser.add_argument("--suffix", type=str, default="_Run")
    parser.add_argument("--head_hadronlist", type=str, default="JetscapeHadronListBin")
    parser.add_argument("--head_sigma", type=str, default="SigmaHardBin")
    args = parser.parse_args()

    Move(args)




if __name__ == '__main__':
    main()
