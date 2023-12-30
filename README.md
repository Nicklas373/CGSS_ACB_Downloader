# IM@S Cinderella Girls Starlight Stage ACB (Only) Assets Downloader Based on Python
This is a python based script that can download ACB assets files for BGM, Sound / Live and Solo directory on database.

# Project Status
![Manifest](https://img.shields.io/badge/dynamic/json.svg?color=blue&label=Manifest&query=truth_version&url=https%3A%2F%2Fstarlight.kirara.ca%2Fapi%2Fv1%2Finfo) ![Static Manifest](https://img.shields.io/badge/Static%20Manifest-10116700-blue) ![Updates](https://img.shields.io/badge/Latest%20Updates-20231118-blue)

Main functions :
1. Check latest manifest version that available on server
2. Download lz4 compressed database and then download assets for BGM, Sound, Solo, SE file in the database
3. Create file to rename all downloaded assets for each hash code file (and you can execute it to get exact name with .acb or .awb file)

What's next :
1. Execute cgss.py to download all data from latest manifests
2. Execute bak.py to create backup from original assets
3. Execute all l_ren%.bat from Sound & Solo backup folder to get codename for each file
   * For rename make sure to changes region -> administrative -> system locale to japanese
   and check UTF-8 support BETA, before doing rename
   
* If audio is acb:
4. Open VGMToolbox -> Misc Tools -> Extraction Tools -> Common Archives -> CRI ACB/AWB Archive Extractor
    - Drop all .acb files in here and wait for extraction process
    - Search and move all .hca files after extract process from VGMToolbox then move to other specific folder
    - Remove extraction folder then run specific rename bat script to correct name from codesong.hca to songtitle~vocalist.hca
    - After sucessfully rename, move all .hca files to Foobar2000 application then convert to .wav
    - Done
5. Do step 4 again for BGM, Sound, Solo and SE to get extracted audio files
    (NOTE: for step 3 only applicable to run once if want to generate new name list)
    
* If audio is awb:
4. After sucessfully rename, move all .awb files to Foobar2000 application then convert to .wav
       
Dependency:
* Python-Modules
1. requests (module)
2. lz4 (module)
3. numpy (module)

* Windows
1. [Python v3.10](https://www.python.org/downloads/release/python-3100/) or [Python v3.8 (Min Requirement)](https://www.python.org/downloads/release/python-380/)
2. [Foobar2000](https://www.foobar2000.org/download)
3. [VGMStream Foobar2000 Plugin](https://vgmstream-builds.s3-us-west-1.amazonaws.com/a3a2baa2999eb1d9f42591e35a4cab5c3445c6a9/windows/foo_input_vgmstream.fb2k-component)
4. [VGMToolbox](https://sourceforge.net/projects/vgmtoolbox/files/latest/download)

NOTE:
1. This script only work on windows for now 
2. You'll need to install python software to execute this file
3. I'm not pro at python, so if any error or you find any error just comment and wait it, i'm not promise to serve quick fix at the moment

Thanks to :
- [ACADFA4/CGSS_ACB_Downloader](https://github.com/ACA4DFA4/CGSS_ACB_Downloader)
- [cisagov/travis-wait-improved](https://github.com/cisagov/travis-wait-improved)
- [CPLs (Nyaa.si)](https://nyaa.si/view/1131944)
- [esterTion/cgss_master_db_diff](https://github.com/esterTion/cgss_master_db_diff)
- [OpenCGSS/DereTore](https://github.com/OpenCGSS/DereTore)
- [Toyobashi/CGSS_ASSET_Downloader](https://github.com/toyobayashi/CGSSAssetsDownloader)

# Copyright
The copyright of CGSS and its related content is held by [BANDAI NAMCO Entertainment Inc.](https://bandainamcoent.co.jp/)

# HANA-CI Build Project || 2016-2023
