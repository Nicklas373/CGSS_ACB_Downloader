#!py -3
#!/usr/bin/env python

def usage():
	print("\tUsage:bak.py")
	return
    
import numpy as np
import os, os.path
import shutil
from pathlib import Path
from os import path

# define the name of the directory to be created
cgss_win_path = os.getcwd()
path_orig = np.array(["bgm/", "sound/", "solo/", "se/"])
path_moved = np.array(["bgm_acb", "sound_acb", "solo_acb", "se_acb"])
f=Path("Static_version")
f=open(f, 'r')
cgss_manifest_ver=f.read()
f.close()
path_backup = cgss_win_path+"//"+cgss_manifest_ver+"//"

# define move all files to specific directory command
i = 0
while i < 4:
    files = os.listdir(path_backup+path_orig[i])
    os.mkdir(path_backup+path_moved[i])
    try:
        shutil.copytree(path_backup+path_orig[i], path_backup+path_moved[i], dirs_exist_ok=True)
    except OSError:
        print("\tCopy files from %s to static directory failed" % path_moved[i])
    else:
        print("\tMoving files from %s to static directory success" % path_moved[i])
    i += 1
            
print("\tScript done, finally :p")
