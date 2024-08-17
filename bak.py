#!py -3
#!/usr/bin/env python

import numpy as np
import os, os.path, sys
import shutil
from pathlib import Path

# define the name of the directory to be created
cgss_win_path = os.getcwd()
path_orig = np.array(["bgm/", "bgm-movie/", "sound/", "solo/", "se/"])
path_moved = np.array(["bgm_acb", "bgm-movie_acb", "sound_acb", "solo_acb", "se_acb"])
if os.path.exists("Static_version"):
    f=Path("Static_version")
    f=open(f, 'r')
    cgss_manifest_ver=f.read()
    f.close()
    path_backup = cgss_win_path+"//"+cgss_manifest_ver+"//"
else:
    print("\tStatic version are not found !")
    print("\tPlease run cgss.py to get manifests version")
    sys.exit(1)

# define move all files to specific directory command
i = 0
while i < len(path_orig):
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
