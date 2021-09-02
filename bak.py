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
    
# remove unused or unindexed files from original directory
i = 0
while i < 4:
    for root, _, files in os.walk(cgss_win_path + cgss_manifest_ver + "/" + path_orig[i]):
        for f in files:
            fullpath = os.path.join(root, f)
            try:
                if os.path.getsize(fullpath) < 7 * 1024:   #set file size in kb
                    print (fullpath)
                    if fullpath.endswith('.bat'):
                        print (fullpath + " was excluded due a bat files")
                    else:
                        print (fullpath + " was removed, size below than 7kb")
                        os.remove(fullpath)
            except WindowsError:
                print ("Error" + fullpath)
    i += 1
            
print ("Script done, finally :p")
