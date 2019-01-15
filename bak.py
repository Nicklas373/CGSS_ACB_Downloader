# import the os module
import os

# import the shutil module (move directory)
import shutil

# define the name of the directory to be created
path_bgm = "bgm/"
path_sound = "sound/"
path_bgm_moved = "bgm_acb"
path_sound_moved = "sound_acb"
success="Good lah :v"

# define move all files to specific directory command
files = os.listdir(path_bgm)

os.mkdir(path_bgm_moved)
try:
    for f in files:
        shutil.copy(path_bgm+f, path_bgm_moved)
except OSError:
    print ("Copy files from %s to static directory failed" % path_bgm_moved)
else:
     print ("Moving files from %s to static directory success" % path_bgm_moved)

# define move all files to specific directory command
files = os.listdir(path_sound)

os.mkdir(path_sound_moved)
try:
    for f in files:
        shutil.copy(path_sound+f, path_sound_moved)
except OSError:
    print ("Copy files from %s to static directory failed" % path_sound_moved)
else:
     print ("Moving files from %s to static directory success" % path_sound_moved)

# execute renaming mass file on the folder
os.system("bgm_acb/b_ren1.bat")
os.system("bgm_acb/b_ren2.bat")
os.system("sound_acb/l_ren1.bat")
os.system("sound_acb/l_ren2.bat")

print ("Script done, finally :p")
