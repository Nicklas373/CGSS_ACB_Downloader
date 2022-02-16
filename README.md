# IM@S Cinderella Girls Starlight Stage ACB (Only) Assets Downloader Based on Python
This is a python based script that can download ACB assets files for BGM, Sound / Live and Solo directory on database.

# Project Status
![Build](https://app.travis-ci.com/Nicklas373/CGSS_ACB_Downloader.svg?branch=master) ![Manifest](https://img.shields.io/badge/dynamic/json.svg?color=blue&label=Manifest&query=truth_version&url=https%3A%2F%2Fstarlight.kirara.ca%2Fapi%2Fv1%2Finfo) ![Static Manifest](https://img.shields.io/badge/Static%20Manifest-10093100-blue) ![Updates](https://img.shields.io/badge/Latest%20Updates-20220216-blue)

How it's work :
1. Script will check latest manifest version that available on server
2. Script will download lz4 compressed database and then download assets for BGM, Sound, Solo, SE file in the database
3. Script will create separate directory for each downloaded assets files
4. Script will create bat file to write exact name for each hash code file (and you can execute it to get exact name with .acb or .awb file)
5. Script complete

What's next :
1. Execute bak.py to create backup from renaming files on MANIFEST_VERSION/bak.py
1. Execute bat files in every directory inside manifest version folder name 
2. Download [DeretoreToolkit](https://github.com/OpenCGSS/DereTore)
4. Extract deretore toolkit and go to folder release
5. Drag and drop your acb file that want to extract to program called "ACB2WAV.exe" on bgm_acb or sound_acb to deretore-toolkit/release
6. WAV files will available on your acb current directory (bgm_acb/sound_acb/solo_acb/solo_part_awb/se_acb)

Dependency:
1. Python v3.8
2. requests (module)
3. lz4 (module)
4. numpy (module)

NOTE:
1. This script only work on windows for now 
2. You'll need to install python software to execute this file
3. I'm not pro at python, so if any error or you find any error just comment and wait it, i'm not promise to serve quick fix at the moment

Thanks to :
- [ACADFA4](https://github.com/ACA4DFA4/CGSS_ACB_Downloader)
- [Toyobashi/CGSS_ASSET_Downloader](https://github.com/toyobayashi/CGSSAssetsDownloader)
- [Deretore Tookit](https://github.com/OpenCGSS/DereTore)
- [CPLs](https://nyaa.si/view/1131944)
- [esterTion](https://github.com/esterTion/cgss_master_db_diff)


# Copyright
The copyright of CGSS and its related content is held by [BANDAI NAMCO Entertainment Inc.](https://bandainamcoent.co.jp/)

# HANA-CI Build Project || 2016-2021
