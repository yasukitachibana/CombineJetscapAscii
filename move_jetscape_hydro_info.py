import os
import sys
import pathlib
import re
import numpy as np
import glob
import shutil

def Move(args):
    


    list = GetFileList()
    cwd = os.getcwd()
    print('\n### Files', list)
    print('### From Directory '+cwd+' to '+args.destination+'\n')

    
    for file in list:
        export = os.path.join(args.destination,file)
        pathlib.Path(export).touch()


        data = np.loadtxt(file)


        event_in_a_file = len(data[:,0])
        for i in range(event_in_a_file):
            data[i,0] = i+1

        with open(export,'a') as f:
            for i in range(args.event_total):
                if int(data[-1,0]) <= args.event_total:
                    np.savetxt(f,data)
                    data[:,0] = data[:,0]+event_in_a_file
                else:
                    f.close()
                    break
#
#        data = np.loadtxt(export)
#        print(data)

def GetFileList():
    return {'SoftAnisotropy_Coefficients_5TeV_0-10.txt','SoftAnisotropy_Coefficients_5TeV_30-40.txt','SoftAnisotropy_Coefficients_5TeV_40-50.txt'}

def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target_directory", type=str, default="/wsu/home/go/go54/go5410/maj-shen/JETSCAPEDataFile/HydroProfiles")
    parser.add_argument("--destination", type=str, default="./test")
    parser.add_argument("--event_total", type=int, default=120000)
    args = parser.parse_args()
    
    home = os.getcwd()
    os.chdir(args.target_directory)
    Move(args)
    os.chdir(home)



if __name__ == '__main__':
    main()
