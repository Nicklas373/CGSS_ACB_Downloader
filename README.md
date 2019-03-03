# IM@S Cinderella Girls Starlight Stage ACB (Only) Assets Downloader Based on Python (Not work for now)
This is a python based script that can download ACB assets files for BGM and Sound / Live directory on database.

# Project Status
![Build](https://img.shields.io/badge/build-partially-yellow.svg) ![Manifest](https://img.shields.io/badge/Manifest-10051920-blue.svg) ![Updates](https://img.shields.io/badge/Latest%20Update-20190223-blue.svg)

How it's work :
1. Script will check latest manifest version that available on server
2. Script will download manifest, following with BGM and Sound file that still in hash name
3. Script will create separate directory for each BGM and Sound acb files
4. Script will create bat file to write exact name for each hash code file (and you can execute it to get exact name with .acb file)
5. Script complete

What's next :
1. Execute bak.py to create backup from renaming files on MANIFEST_VERSION/bak.py
1. Execute b_ren1.bat,b_ren2.bat to rename files to acb from MANIFEST_VERSION/bgm_acb and l_ren1.bat, l_ren2.bat to acb from MANIFEST_VERSION/sound_acb 
2. Download [DeretoreToolkit](https://github.com/OpenCGSS/DereTore)
4. Extract deretore toolkit and go to folder release
5. Drag and drop your acb file that want to extract to program called "ACB2WAV.exe" on bgm_acb or sound_acb to deretore-toolkit/release
6. WAV files will available on your acb current directory (bgm_acb/sound_acb)

NOTE:
1. This script only work on windows for now 
2. You'll need to install python software to execute this file
3. I'm not pro at python, so if any error or you find any error just comment and wait it, i'm not promise to serve quick fix at the moment

Thanks to :
- [ACADFA4](https://github.com/ACA4DFA4/CGSS_ACB_Downloader)
- [Toyobashi/CGSS_ASSET_Downloader](https://github.com/toyobayashi/CGSSAssetsDownloader)
- [Deretore Tookit](https://github.com/OpenCGSS/DereTore)
- [CPLs](https://nyaa.si/view/1117762)
