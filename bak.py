# import the os module
import os

# import the shutil module (move directory)
import shutil

# define the name of the directory to be created
path_bgm = "bgm/"
path_sound = "sound/"
path_solo = "solo/"
path_se = "se/"
path_bgm_moved = "bgm_acb"
path_sound_moved = "sound_acb"
path_solo_moved = "solo_acb"
path_se_moved = "se_acb"

# define move all files to specific directory command
files = os.listdir(path_bgm)

os.mkdir(path_bgm_moved)
try:
    shutil.copytree(path_bgm, path_bgm_moved, dirs_exist_ok=True)
except OSError:
    print ("Copy files from %s to static directory failed" % path_bgm_moved)
else:
     print ("Moving files from %s to static directory success" % path_bgm_moved)

# define move all files to specific directory command
files = os.listdir(path_sound)

os.mkdir(path_sound_moved)
try:
    shutil.copytree(path_sound, path_sound_moved, dirs_exist_ok=True)
except OSError:
    print ("Copy files from %s to static directory failed" % path_sound_moved)
else:
     print ("Moving files from %s to static directory success" % path_sound_moved)

# define move all files to specific directory command
files = os.listdir(path_solo)

os.mkdir(path_solo_moved)
try:
    shutil.copytree(path_solo, path_solo_moved, dirs_exist_ok=True)
except OSError:
    print ("Copy files from %s to static directory failed" % path_solo_moved)
else:
     print ("Moving files from %s to static directory success" % path_solo_moved)

# define move all files to specific directory command
files = os.listdir(path_se)

os.mkdir(path_se_moved)
try:
    shutil.copytree(path_se, path_se_moved, dirs_exist_ok=True)
except OSError:
    print ("Copy files from %s to static directory failed" % path_se_moved)
else:
     print ("Moving files from %s to static directory success" % path_se_moved)
     
print ("Script done, finally :p")
