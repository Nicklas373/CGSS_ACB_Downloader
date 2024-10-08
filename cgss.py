#!py -3
#!/usr/bin/env python

import csv
import json
import numpy as np
import requests
import shutil
import sqlite3,hashlib
import os,sys, os.path
import time
from datetime import date
from lz4 import block
from pathlib import Path
from os import path

platform='iOS'

def dlfilefrmurl(url,path,headers):
	r=requests.get(url,headers=headers)
	fp=open(path,'wb')
	fp.write(r.content)
	fp.close()
	ldate=r.headers['Last-Modified']
	timeStruct=time.strptime(ldate,"%a, %d %b %Y %H:%M:%S GMT")
	timestamp=time.mktime(timeStruct)+8*60*60
	os.utime(path,(os.stat(path).st_atime,timestamp))
	r.close()

suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

cgss_path=os.getcwd()
cgss_logs=cgss_path+"\\logs"
csv_header= ['name', 'hash', 'size', 'date', 'manifest_version']

try:
        print("\tCGSS ACB Downloader | Starting!")
        print("\tfrom @ACA4DFA4 | Update & Maintain by @Nicklas373")
        url="https://starlight.kirara.ca/api/v1/info"
        r=requests.get(url)
        jsonData=json.loads(r.content)
        version=jsonData['truth_version']
except Exception as e:
        print("\tStarlight kirara was down...")
        print("\tGetting game version from esterTion source...")
        url="https://raw.githubusercontent.com/esterTion/cgss_master_db_diff/master/!TruthVersion.txt"
        r=requests.get(url)
        version=r.text.rstrip()
else:
        print("")

if os.path.exists(cgss_path+"\\Static_version"):
        f=Path(cgss_path+"\\Static_version")
        f=open(f)
        version_orig = f.read()
        f.close()
else:
        f=Path(cgss_path+"\\Static_version")
        f=open(f, 'w')
        f.write("000000")
        f.close()
        version_orig = "000000"

if version_orig == "":
        version_orig = "000000"

print("\tCurrent manifest version = "+version_orig)
print("\tNew manifest version = "+version)
if os.path.exists(cgss_path+"\\"+version_orig):
        if version_orig < version:
                print("\tCurrent version with the latest manifest is outdated")
                if not os.path.exists(cgss_path+"\\"+version):
                        os.mkdir(cgss_path+"\\"+version)
                if os.path.exists(cgss_path+"\\"+version_orig):
                        old_manifest=os.listdir(cgss_path+"\\"+version_orig)
                        try:
                                print("\tMoving files from current manifest to latest manifest ...")
                                for x in old_manifest:
                                        shutil.move(cgss_path+"\\"+version_orig+"\\"+x,cgss_path+"\\"+version+"\\"+x)
                        except OSError:
                                print("\tCopy files from %s to static directory failed" % version)
                        print("\tRemoving old manifest files ...")
                        shutil.rmtree(cgss_path+"\\"+version_orig)
                else:
                        print("\tPrevious manifest files: "+version_orig+" are not found !")
                        print("\tAbort moving to new manifests !")
                f=Path("Static_version")
                f=open(f, 'w')
                f.write(version)
                f.close()
                print("\tRe-writing old static manifest with the latest one")
                f=Path(cgss_path+"\\.gitignore")
                f=open(f, 'a')
                f.write("\n"+version+"/")
                f.close()
                print("\tRe-writing new manifest into .gitignore")
        elif version_orig == version:
                print("\tCurrent version with the latest manifest is same")
                print("\tRe-checking manifest ...")
        elif version_orig > version:
                print("\tCurrent version with the latest manifest is unknown")
                sys.exit(1)
else:
        if not os.path.exists(cgss_path+"\\"+version):
                os.mkdir(cgss_path+"\\"+version)
        f=Path("Static_version")
        f=open(f, 'w')
        f.write(version)
        f.close()
        print("\tRe-writing static manifest with the latest one")
        f=Path(cgss_path+"\\.gitignore")
        f=open(f, 'a')
        f.write("\n"+version+"/")
        f.close()
        print("\tRe-writing new manifest into .gitignore")
        
if not os.path.exists(cgss_logs):
        os.makedirs(cgss_logs)
if not os.path.exists(cgss_path+"\\"+version+"\\solo"):
        os.makedirs(cgss_path+"\\"+version+"\\solo")

android_headers={'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; Nexus 42 Build/XYZZ1Y)','X-Unity-Version': '2017.4.2f2','Accept-Encoding': 'gzip','Connection' : 'Keep-Alive','Accept' : '*/*'}
ios_headers={'User-Agent': 'BNEI0242/96 CFNetwork/808.2.16 Darwin/16.3.01','RES_VER': version,'APP_VER': '10.3.5','OS_VER': 'iPhone OS 10.2','X-Unity-Version': '2017.4.2f2','Accept-Encoding': 'gzip','Connection' : 'Keep-Alive','Accept' : '*/*','DEVICE_ID': '10FB122A-CC47-4B10-8C78-0D1E6C22119C','DEVICE_NAME': 'iPhone8,1','USER_AGENT': 'BNEI0242/96 CFNetwork/808.2.16 Darwin/16.3.01','IP_ADDRESS': '192.168.12.14','GPU_NAME': 'Apple A9 GPU','KEYCHAIN': '339871861','CARRIER': 'KDDI','IDFA': '3350E88E-ED66-4D46-8B28-D82EA4A6397D'}

if platform != None:
        if platform == 'Android':
                headers=android_headers
                platform='Android'
        elif platform == 'iOS':
                headers=ios_headers
                platform='iOS'
        else:
                headers=android_headers
                platform='Android'
else:
        headers=android_headers
        platform='Android'

if not os.path.exists(cgss_path+"\\manifests"):
	os.mkdir(cgss_path+"\\\\manifests")
dbname=cgss_path+"\\manifests\\manifest_"+version+".db"
lz4name=cgss_path+"\\manifests\\manifest_"+version+".db.lz4"
if not os.path.exists(dbname):
	if not os.path.exists(lz4name):
		print("\tDownloading lz4-compressed database ...")
		url="http://asset-starlight-stage.akamaized.net/dl/"+version+"/manifests/"+platform+"_AHigh_SHigh"
		r=requests.get(url,headers=headers)
		with open(lz4name,'wb') as fp:
			fp.write(r.content)
			fp.close()
		ldate=r.headers['Last-Modified']
		timeStruct=time.strptime(ldate,"%a, %d %b %Y %H:%M:%S GMT")
		timestamp=time.mktime(timeStruct)+8*60*60
		os.utime(lz4name,(os.stat(lz4name).st_atime,timestamp))
		dat=r.content[4:]
		r.close()
	else:
		fp=open(lz4name,'rb')
		dat=fp.read()[4:]
		fp.close()
	dat=dat[0:4]+dat[12:]
	dec=block.decompress(dat)
	fp=open(dbname,'wb')
	fp.write(dec)
	fp.close()
	del(dec)
	del(dat)

print("\tAnalysing sqlite3 database ...\n")
db=sqlite3.Connection(dbname)

song_in_folder = np.array(["bgm", "bgm-movie","sound", "se"])
song_in_alias = np.array(["b", "m", "l", "s"])
i = 0
while i < len(song_in_folder):
        csv_path=cgss_logs+"\\csv\\"+song_in_folder[i]+".csv"
        print("\tDownloading assets for: "+song_in_folder[i]+"...")
        query=db.execute("select name,hash,size from manifests where name like '"+song_in_alias[i]+"/%.acb' and size > '7000'")
        cgss_folder=cgss_path+"\\"+version+"\\"+song_in_folder[i]
        if not os.path.exists(version+"\\"+song_in_folder[i]+"\\"):
            os.makedirs(cgss_folder)
        fp1=open(cgss_path+"\\"+version+"\\"+song_in_folder[i]+"\\"+song_in_alias[i]+"_ren1.bat",'w')
        fp2=open(cgss_path+"\\"+version+"\\"+song_in_folder[i]+"\\"+song_in_alias[i]+"_ren2.bat",'w')
        today=date.today()
        if not os.path.exists(csv_path):
                if not os.path.exists(cgss_logs+"\\csv\\"):
                        os.makedirs(cgss_logs+"\\csv\\")
                f = open(csv_path, 'w', encoding='UTF8', newline='')
                writer = csv.writer(f)
                writer.writerow(csv_header)
                f.close()    
        for name,hash,size in query:
                fp1.write("ren "+hash+' '+name[2:]+'\n')
                fp2.write("ren "+name[2:]+' '+hash+'\n')
                if not os.path.exists(cgss_path+"\\"+version+"\\"+song_in_folder[i]+"\\"+hash):
                        csv_rows=[name[2:], hash, humansize(size), today, version]
                        f = open(csv_path, 'a', encoding='UTF8', newline='')
                        writer = csv.writer(f)
                        writer.writerow(csv_rows)
                        f.close()        
                        url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                        dlfilefrmurl(url,version+"\\"+song_in_folder[i]+"\\"+hash,headers)
                        print("\tDownloading assets: "+name[2:]+"...")
                else:
                        fp=Path(cgss_path+"\\"+version+"\\"+song_in_folder[i]+"\\"+hash)
                        fp.touch(exist_ok=True)
                        fp=open(fp,'rb')
                        buf=fp.read()
                        fp.close()
                        md5res=hashlib.md5(buf).hexdigest()
                        del(buf)
                        if md5res!=hash:
                                print("\tFile "+hash+'('+name+')'+" didn't pass md5check, delete and re-downloading ...")
                                url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                                dlfilefrmurl(url,version+"\\"+song_in_folder[i]+"\\"+hash,headers)
                                print("\tDownloading assets: "+name[2:]+"...")
        fp1.close()
        fp2.close()
        i += 1
      
query=db.execute("select name,hash,size from manifests where name like 'l/song_%_part/inst_song_%.awb' and name not like 'l/song_%_part/inst_song_%_se.awb' and name not like 'l/song_%_part/inst_song_%_another.awb'")

if not os.path.exists(cgss_logs+"\\txt\\"):
        os.makedirs(cgss_logs+"\\txt\\")

if os.path.isfile(cgss_logs+"\\txt\\"+"solo_list.txt"):
        os.remove(cgss_logs+"\\txt\\"+"solo_list.txt")
        
for name,hash,size in query:
        f=open(cgss_logs+"\\txt\\"+"solo_list.txt", 'a')
        if "_se" in name:
                f.write(name[2:][:-21]+"\n")
        else:
                f.write(name[2:][:-19]+"\n")
        f.close()

solo_list = np.loadtxt(cgss_logs+"\\txt\\"+"solo_list.txt", dtype=str, delimiter=",") 
for song_in_query in solo_list:
        print("\tDownloading assets for: "+song_in_query+"...")
        query=db.execute("select name,hash,size from manifests where name like 'l/"+song_in_query+"/%.awb' and name not like 'l/song_%_part/inst_song_%_another.awb'")
        part=cgss_path+"\\"+version+"\\solo\\"+song_in_query
        if not os.path.exists(part):
                os.makedirs(part)
        csv_solo_path=cgss_logs+"\\csv\\"+song_in_query+".csv"
        today=date.today()
        if not os.path.exists(csv_solo_path):
                if not os.path.exists(cgss_logs+"\\csv\\"):
                        os.makedirs(cgss_logs+"\\csv\\")
                f = open(csv_solo_path, 'w', encoding='UTF8', newline='')
                writer = csv.writer(f)
                writer.writerow(csv_header)
                f.close() 
        for name,hash,size in query:
                fp1=open(cgss_path+"\\"+version+"\\solo\\"+song_in_query+"\\p_ren1.bat",'a')
                fp2=open(cgss_path+"\\"+version+"\\solo\\"+song_in_query+"\\p_ren2.bat",'a')
                fp1.write("ren "+hash+' '+name[17:]+'\n')
                fp2.write("ren "+name[17:]+' '+hash+'\n')
                if not os.path.exists(cgss_path+"\\"+version+"\\solo\\"+song_in_query+"\\"+hash):
                        csv_solo_rows=[name[2:], hash, humansize(size), today, version]
                        f = open(csv_solo_path, 'a', encoding='UTF8', newline='')
                        writer = csv.writer(f)
                        writer.writerow(csv_solo_rows)
                        f.close()
                        url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                        dlfilefrmurl(url,version+"\\solo\\"+song_in_query+"\\"+hash,headers)
                        print("\tDownloading assets: "+name[17:]+"...")
                else:
                        fp=Path(cgss_path+"\\"+version+"\\solo\\"+song_in_query+"\\"+hash)
                        fp.touch(exist_ok=True)
                        fp=open(fp,'rb')
                        buf=fp.read()
                        fp.close()
                        md5res=hashlib.md5(buf).hexdigest()
                        del(buf)
                        if md5res!=hash:
                                print("\tFile "+hash+'('+name+')'+" didn't pass md5check, delete and re-downloading ...")
                                url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                                dlfilefrmurl(url,version+"\\solo\\"+song_in_query+"\\"+hash,headers)
                                print("\tDownloading assets: "+name[17:]+"...")
        fp1.close()
        fp2.close()
        
query=db.execute("select name,hash,size from manifests where name like 'l/song_%_part/inst_song_%_another.awb'")
if os.path.isfile(cgss_logs+"\\txt\\"+"solo_list_another.txt"):
        os.remove(cgss_logs+"\\txt\\"+"solo_list_another.txt")
        
for name,hash,size in query:
        f=open(cgss_logs+"\\txt\\"+"solo_list_another.txt", 'a')
        f.write(name[2:][:-27]+"\n")
        f.close()

solo_list = np.loadtxt(cgss_logs+"\\txt\\"+"solo_list_another.txt", dtype=str, delimiter=",") 
for song_in_query in solo_list:
        new_song_code=song_in_query[5:][:-5]
        print("\tDownloading assets for: "+song_in_query+"_another...")
        query=db.execute("select name,hash,size from manifests where name like 'l/"+song_in_query+"/inst_song_"+new_song_code+"_%.awb'")
        part=cgss_path+"\\"+version+"\\solo\\"+song_in_query+"_another"
        if not os.path.exists(part):
               os.makedirs(part)
        csv_solo_path=cgss_logs+"\\csv\\"+song_in_query+"_another.csv"
        today=date.today()
        if not os.path.exists(csv_solo_path):
                if not os.path.exists(cgss_logs+"\\csv\\"):
                        os.makedirs(cgss_logs+"\\csv\\")
                f = open(csv_solo_path, 'w', encoding='UTF8', newline='')
                writer = csv.writer(f)
                writer.writerow(csv_header)
                f.close() 
        for name,hash,size in query:
                fp1=open(cgss_path+"\\"+version+"\\solo\\"+song_in_query+"_another\\p_ren1.bat",'a')
                fp2=open(cgss_path+"\\"+version+"\\solo\\"+song_in_query+"_another\\p_ren2.bat",'a')
                fp1.write("ren "+hash+' '+name[17:]+'\n')
                fp2.write("ren "+name[17:]+' '+hash+'\n')
                if not os.path.exists(version+"\\solo\\"+song_in_query+"_another\\"+hash):
                        csv_solo_rows=[name[2:], hash, humansize(size), today, version]
                        f = open(csv_solo_path, 'a', encoding='UTF8', newline='')
                        writer = csv.writer(f)
                        writer.writerow(csv_solo_rows)
                        f.close()
                        url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                        dlfilefrmurl(url,version+"\\solo\\"+song_in_query+"_another\\"+hash,headers)
                        print("\tDownloading assets: "+name[17:]+"...")
                else:
                        fp=Path(cgss_path+"\\"+version+"\\solo\\"+song_in_query+"_another\\"+hash)
                        fp.touch(exist_ok=True)
                        fp=open(fp,'rb')
                        buf=fp.read()
                        fp.close()
                        md5res=hashlib.md5(buf).hexdigest()
                        del(buf)
                        if md5res!=hash:
                                print("\tFile "+hash+'('+name+')'+" didn't pass md5check, delete and re-downloading ...")
                                url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                                dlfilefrmurl(url,version+"\\solo\\"+song_in_query+"_another\\"+hash,headers)
                                print("\tDownloading assets: "+name[17:]+"...")
        fp1.close()
        fp2.close()
        
query=db.execute("select name,hash,size from manifests where name like 'l/song_%_part/inst_song_%_another.awb'")
if os.path.isfile(cgss_logs+"\\txt\\"+"solo_list_another.txt"):
        os.remove(cgss_logs+"\\txt\\"+"solo_list_another.txt")
        
for name,hash,size in query:
        f=open(cgss_logs+"\\txt\\"+"solo_list_another.txt", 'a')
        f.write(name[2:][:-27]+"\n")
        f.close()

solo_list = np.loadtxt(cgss_logs+"\\txt\\"+"solo_list_another.txt", dtype=str, delimiter=",") 
for song_in_query in solo_list:
        new_song_code=song_in_query[5:][:-5]
        print("\tDownloading assets for: "+song_in_query+"_another...")
        query=db.execute("select name,hash,size from manifests where name like 'l/"+song_in_query+"/inst_song_"+new_song_code+"_%.awb'")
        part=cgss_path+"\\"+version+"\\solo\\"+song_in_query+"_another"
        if path.exists(part):
                print("")
        else:
                os.makedirs(part)
        csv_solo_path=cgss_logs+"\\csv\\"+song_in_query+"_another.csv"
        fp1=open(cgss_path+"\\"+version+"\\solo\\"+song_in_query+"_another\\p_ren1.bat",'a')
        fp2=open(cgss_path+"\\"+version+"\\solo\\"+song_in_query+"_another\\p_ren2.bat",'a')
        today=date.today()
        if not os.path.exists(csv_solo_path):
                f = open(csv_solo_path, 'w', encoding='UTF8', newline='')
                writer = csv.writer(f)
                writer.writerow(csv_header)
                f.close() 
        for name,hash,size in query:
                fp1.write("ren "+hash+' '+name[17:]+'\n')
                fp2.write("ren "+name[17:]+' '+hash+'\n')
                if not os.path.exists(cgss_path+"\\"+version+"\\solo\\"+song_in_query+"_another\\"+hash):
                        csv_solo_rows=[name[2:], hash, humansize(size), today, version]
                        f = open(csv_solo_path, 'a', encoding='UTF8', newline='')
                        writer = csv.writer(f)
                        writer.writerow(csv_solo_rows)
                        f.close()
                        url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                        dlfilefrmurl(url,version+"\\solo\\"+song_in_query+"_another\\"+hash,headers)
                        print("\tDownloading assets: "+name[17:]+"...")
        fp1.close()
        fp2.close()
        
print("\tCGSS ACB Downloader | Finished!")
