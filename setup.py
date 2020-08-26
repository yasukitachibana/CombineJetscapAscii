import os
import get_filenames as gf
import set_xml as sxml
import get_command as gcom
import manage_dir as mdir
import generate_qsub_command as qcom
import set_path as spath


def GetXml(argc, argvs, master_xml, xml_filename, this_bin, eCM):
    
    PPAA = argvs[2]
    master = open(master_xml).read()
    copy = master
    
    copy = sxml.SetXmlParam( 'Random',copy,'seed', 0 )
    
    copy = sxml.SetXmlParam( 'PythiaGun',copy,'FSR_on', 0 )
    copy = sxml.SetXmlParam( 'PythiaGun',copy,'pTHatMin', this_bin[0] )
    copy = sxml.SetXmlParam( 'PythiaGun',copy,'pTHatMax', this_bin[1] )
    copy = sxml.SetXmlParam( 'PythiaGun',copy,'eCM', eCM )
    copy = sxml.SetXmlParam( 'PythiaGun',copy,'useHybridHad', 0 )
    
    copy = sxml.SetXmlParam( 'Eloss',copy,'deltaT', 0.1 )
    copy = sxml.SetXmlParam( 'Eloss',copy,'formTime', -0.1 )
    copy = sxml.SetXmlParam( 'Eloss',copy,'maxT', 250 )
    copy = sxml.SetXmlParam( 'Eloss',copy,'mutex', 'ON' )
    
    copy = sxml.SetXmlParam( 'JetHadronization',copy,'eCMforHadronization', 0.5*eCM )
    
    copy = sxml.SetXmlParam( 'Matter',copy,'useHybridHad', 0 )
    copy = sxml.SetXmlParam( 'Matter',copy,'matter_on', 1 )
    copy = sxml.SetXmlParam( 'Matter',copy,'vir_factor', 0.25 )
    copy = sxml.SetXmlParam( 'Matter',copy,'broadening_on', 0 )
    copy = sxml.SetXmlParam( 'Matter',copy,'brick_med', 0 )
    copy = sxml.SetXmlParam( 'Matter',copy,'brick_length', 0 )
    copy = sxml.SetXmlParam( 'Matter',copy,'qhat0', -3.0 )

    if PPAA == 'PP':
        copy = SetXmlPP(copy)
    else:
        copy = SetXmlAA(argc, argvs, copy)
    
    
    xml_file = open(xml_filename,'w')
    xml_file.write(copy)
    xml_file.close

def SetXmlPP(copy):

    copy = sxml.SetXmlParam( 'Matter',copy,'Q0', 1.0 )
    copy = sxml.SetXmlParam( 'Matter',copy,'in_vac', 1 )
    copy = sxml.SetXmlParam( 'Matter',copy,'recoil_on', 0 )
    copy = sxml.SetXmlParam('Matter',copy,'alphas', 0.0 )
    
    return copy

def SetXmlAA(argc, argvs, copy):

    hydro_files_folder = spath.HydroFilePath(argvs[3])
    alphas = argvs[4]
    Qs = argvs[5]
    take_recoil = argvs[6]
    T0 = 0.16 #Note! This becomes Tc in LBT
    Tc = 0.15

    copy = sxml.SetXmlParam( 'IS',copy,'initial_profile_path', hydro_files_folder )
    copy = sxml.SetXmlParam( 'hydro_from_file',copy,'hydro_files_folder', hydro_files_folder )


    if float(Qs)<0.0:
        copy = sxml.SetXmlParam( 'Matter',copy,'Q0', 1.0 )
        copy = sxml.SetXmlParam( 'Lbt',copy,'Q0', 1.0 )
    else:
        copy = sxml.SetXmlParam( 'Matter',copy,'Q0', Qs )
        copy = sxml.SetXmlParam( 'Lbt',copy,'Q0', Qs )

    copy = sxml.SetXmlParam( 'Matter',copy,'T0', T0 )
    copy = sxml.SetXmlParam( 'Matter',copy,'in_vac', 0 )
    copy = sxml.SetXmlParam( 'Matter',copy,'recoil_on', 1 )
    copy = sxml.SetXmlParam( 'Matter',copy,'hydro_Tc', Tc )
    copy = sxml.SetXmlParam( 'Matter',copy,'alphas', alphas )

    copy = sxml.SetXmlParam( 'Lbt',copy,'in_vac', 0 )
    copy = sxml.SetXmlParam( 'Lbt',copy,'only_leading', 0 )
    copy = sxml.SetXmlParam( 'Lbt',copy,'hydro_Tc', 0.16 )
    copy = sxml.SetXmlParam( 'Lbt',copy,'qhat0', -3.0 )
    copy = sxml.SetXmlParam( 'Lbt',copy,'alphas', alphas )
        
    copy = sxml.SetXmlParam( 'JetHadronization',copy,'take_recoil', take_recoil )
    
    return copy


def Submit(argc,argvs,code_path,this_bin,run):
    
    script_dir = os.getcwd()
    print('run '+str(run))
    eCM = int(argvs[1])
    PPAA = argvs[2]


    outdir = os.path.join(spath.GetOutputPath(),gf.GetOutdirname(argc,argvs))
    mdir.Mkdirs(outdir)
    master_xml = spath.GetMasterXmlPath()

    exec_name = 'PythiaBrickTest'
    if PPAA != 'PP':
        centrality = argvs[3]
        Qs = argvs[5]
        exec_name = 'hydroJetTest'
        if float(Qs) < 0.0:
            exec_name = exec_name+'MATTER'
        if centrality == '0-10':
            exec_name = exec_name+'Central'
        else:
            exec_name = exec_name+'Peripheral'
            
    xml_filename = os.path.join(outdir,gf.GetXmlFilename(this_bin,run))
    sigma_filename = os.path.join(outdir,gf.GetSigmaFilename(this_bin,run))
    hadron_filename = os.path.join(outdir,gf.GetHadronListFilename(this_bin,run))
    parton_filename = os.path.join(outdir,gf.GetPartonListFilename(this_bin,run))
    out_filename = os.path.join(outdir,gf.GetTestOutFilename(this_bin,run))
    build_dir = os.path.join(outdir,gf.GetBuidDirName(this_bin,run))
    
    GetXml(argc, argvs, master_xml, xml_filename, this_bin, eCM)
    
    command = gcom.GetCommand(code_path, build_dir, exec_name, xml_filename, out_filename, sigma_filename, hadron_filename, parton_filename)
    
    mdir.Mkdirs(build_dir)
    
    command_run = '"python run.py '+command+'"'
    
    master_command = os.path.join(script_dir,'JobMaster')+' '+script_dir+' '+command_run
    #print(master_command)
    
    qsub_command = qcom.GenerateQsubCommand(gf.GetJobName(this_bin,run),master_command)
    
    #print('Submission, Main Command')
    #print(master_command)
    #print('-')
    #os.system(master_command)
    #exit()
    
    print('Submission, Qsub Command')
    print(qsub_command)
    print('-')
    os.system(qsub_command)





