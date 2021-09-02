# import the os module
import os, os.path

# import the shutil module (move directory)
import shutil

# import the numpy module (for array)
import numpy as np

# define the name of the directory to be created
cgss_win_path = "C:/Users/Nickl/Downloads/GitHub/CGSS_ACB_Downloader"
cgss_manifest_ver = "/10087800"
path_orig = np.array(["bgm/", "sound/", "solo/", "se/"])
path_moved = np.array(["bgm_acb", "sound_acb", "solo_acb", "se_acb"])

# define move all files to specific directory command
i = 0
while i < 4:
    files = os.listdir(path_orig[i])
    os.mkdir(path_moved[i])
    try:
        shutil.copytree(path_orig[i], path_moved[i], dirs_exist_ok=True)
    except OSError:
        print ("Copy files from %s to static directory failed" % path_moved[i])
    else:
        print ("Moving files from %s to static directory success" % path_moved[i])
    i += 1
     
print ("Script done, finally :p")
