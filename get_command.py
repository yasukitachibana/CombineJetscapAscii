def GetCommand(code_path, build_dir, exec_name, xml_filename, out_filename, sigma_filename, hadron_filename, parton_filename):

    cd_com = 'cd '+ build_dir
    cmake_com =GetCmakeCommand(code_path,'')
    make_com = GetMakeCommand('')
    exec_com = GetExecCommand(exec_name, xml_filename, out_filename, sigma_filename)
    hadron_com = GetListCommand(out_filename, hadron_filename, 'Hadrons' )
    parton_com = GetListCommand(out_filename, parton_filename, 'Partons' )
    last_com = 'cd ../ ; rm -r ' + build_dir

    # return cd_com + ' ; '+cmake_com+ ' ; '+make_com+' ; '+exec_com+' ; '+hadron_com + ' ; '+parton_com + ' ; '+ last_com
    return cd_com + ' ; '+cmake_com+ ' ; '+make_com+' ; ' +parton_com + ' ; '+ last_com

def GetCmakeCommand(code_path, opt):
    return 'cmake '+opt+' '+code_path

def GetMakeCommand(opt):
    return 'make '+opt

def GetExecCommand(exec_name, xml_filename, out_filename, sigma_filename):
    return './' + exec_name +' '+  xml_filename +' '+ out_filename +' '+ sigma_filename

def GetListCommand(out_filename, list_filename, hadrons_partons ):
    return './FinalState'+hadrons_partons+ ' ' + out_filename +' '+ list_filename
