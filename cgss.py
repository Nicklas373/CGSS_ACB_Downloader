#!py -3
#!/usr/bin/env python

def usage():
	print("\tUsage:run.py [-v <VERSION>] [-g] [-s] [-m]")
	return

import os,sys, os.path
from os import path
from datetime import date
from pathlib import Path
import requests
import json
import sqlite3,hashlib
from lz4 import block
import time
import shutil
import numpy as np

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

version=None
gennamelist=False
verbose=True
md5chk=False
cgss_win_path=os.getcwd()
cgss_logs=cgss_win_path+"\\logs"
args=iter(sys.argv[1:])
for i in args:
	if i=='-v' or i=='--version' or i=='-V' or i=='--version':
		try:
			version=next(args)
		except Exception as e:
			print("\tError:Cannot parse args:"+i,sys.stderr)
			usage()
			sys.exit(1)
	elif i=='-g' or i=='--generate-name-list':
		gennamelist=True
	elif i=='-s' or i=='S' or i=='--silent':
		verbose=False
	elif i=='-m' or i[:5]=='--md5' or i=='--check':
		md5chk=True
	else:
		print("\tError:Cannot parse args:"+i,sys.stderr)
		usage()
		sys.exit(1)

if not version:
        if verbose:
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

if verbose:
        f=Path("Static_version")
        f=open(f)
        version_orig = f.read()
        f.close()
        print("\tCurrent manifest version = "+version_orig)
        print("\tNew manifest version = "+version)
        if path.exists(version_orig):
                if version_orig < version:
                        print("\tCurrent version with the latest manifest is outdated")
                        os.mkdir(".\\"+version)
                        old_manifest=os.listdir(".\\"+version_orig)
                        try:
                                print("\tMoving files from current manifest to latest manifest ...")
                                for x in old_manifest:
                                        shutil.move(".\\"+version_orig+"\\"+x,".\\"+version+"\\"+x)
                        except OSError:
                                print("\tCopy files from %s to static directory failed" % version)
                        print("\tRemoving old manifest files ...")
                        shutil.rmtree(".\\"+version_orig)
                        f=Path("Static_version")
                        f=open(f, 'w')
                        f.write(version)
                        f.close()
                        print("\tRe-writing old static manifest with the latest one")
                elif version_orig == version:
                        print("\tCurrent version with the latest manifest is same")
                        print("\tRe-checking manifest ...")
                elif version_orig > version:
                        print("\tCurrent version with the latest manifest is unknown")
                        sys.exit(1)
                else:
                        os.mkdir(version)
        if path.exists(cgss_logs):
                print("")
        else:
                os.makedirs(cgss_logs)
        if path.exists(cgss_win_path+version+"\\solo"):
                print("")
        else:
                os.makedirs(cgss_win_path+version+"\\solo")
                        
dl_headers={'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; Nexus 42 Build/XYZZ1Y)','X-Unity-Version': '2017.4.2f2','Accept-Encoding': 'gzip','Connection' : 'Keep-Alive','Accept' : '*/*'}

if not os.path.exists(".\\manifests"):
	os.mkdir(".\\manifests")
dbname=".\\manifests\\manifest_"+version+".db"
lz4name=".\\manifests\\manifest_"+version+".db.lz4"
if not os.path.exists(dbname):
	if not os.path.exists(lz4name):
		if verbose:
			print("\tDownloading lz4-compressed database ...")
		url="https://asset-starlight-stage.akamaized.net/dl/"+version+"/manifests/Android_AHigh_SHigh"
		r=requests.get(url,headers=dl_headers)
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

if verbose:
	print("\tAnalysing sqlite3 database ...")
db=sqlite3.Connection(dbname)
if gennamelist:
	if verbose:
		print("\tGenerating namelist.csv ...")
	namelist=open(version+"\\list_name_hash_sha1.csv",'w')
	query=db.execute("select name,hash from manifests")
	namelist.write("name,md5,sha1\n")
	for i in query:
		name,hash=i
		namelist.write(name+','+hash[:2]+hash+',')
		if name[1]=='/':
			name=name[2:]
		namelist.write(hashlib.sha1(name.encode()).hexdigest()+'\n')
	query.close()
	namelist.close()
	
song_in_folder = np.array(["bgm", "sound", "se"])
song_in_alias = np.array(["b", "l", "s"])
i = 0
while i < 3:
        print("\tDownloading assets for: "+song_in_folder[i]+"...")
        query=db.execute("select name,hash,size from manifests where name like '"+song_in_alias[i]+"/%.acb'")
        cgss_folder=version+"\\"+song_in_folder[i]
        if path.exists(version+"\\"+song_in_folder[i]+"\\"):
            print("")
        else:
            os.makedirs(cgss_folder)
        fp1=open(version+"\\"+song_in_folder[i]+"\\"+song_in_alias[i]+"_ren1.bat",'w')
        fp2=open(version+"\\"+song_in_folder[i]+"\\"+song_in_alias[i]+"_ren2.bat",'w')
        today=date.today()
        f=open(cgss_logs+"\\"+song_in_folder[i]+".txt", 'a')
        f.write("---------------"+str(today)+"---------------\n")
        f.write("Current Manifest Version: "+str(version)+"\n")
        f.close()
        for name,hash,size in query:
                fp1.write("ren "+hash+' '+name[2:]+'\n')
                fp2.write("ren "+name[2:]+' '+hash+'\n')
                if not os.path.exists(version+"\\"+song_in_folder[i]+"\\"+hash):
                        if verbose:
                                f=open(cgss_logs+"\\"+song_in_folder[i]+".txt", 'a')
                                f.write(name[2:]+" | "+hash+" | "+humansize(size)+"\n")
                                f.close()
                        url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                        dlfilefrmurl(url,version+"\\"+song_in_folder[i]+"\\"+hash,dl_headers)
                else:
                        if md5chk:
                                with open("\\"+song_in_folder[i]+"\\"+hash,'rb') as fp:
                                        buf=fp.read()
                                        fp.close()
                                        md5res=hashlib.md5(buf).hexdigest()
                                        del(buf)
                                if md5res!=hash:
                                        if verbose:
                                                print("\tFile "+hash+'('+name+')'+" didn't pass md5check, delete and re-downloading ...")
                                                url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                                                dlfilefrmurl(url,version+"\\"+song_in_folder[i]+"\\"+hash,dl_headers)
                                elif verbose:
                                        print("\tFile "+hash+'('+name+')'+" already exists")
        fp1.close()
        fp2.close()
        f=open(cgss_logs+"\\"+song_in_folder[i]+".txt", 'a')
        f.write("----------------------------------------\n")
        f.close()
        i += 1
        
song_part_list = np.array(["song_1009_part", "song_1010_part", "song_1011_part", "song_1201_part", "song_2001_part", "song_2004_part", "song_2005_part", "song_2006_part", "song_2007_part", "song_2010_part", "song_5005_part", "song_5007_part", "song_9003_part", "song_9004_part", "song_9008_part", "song_9012_part", "song_9014_part", "song_9015_part", "song_9017_part", "song_9024_part", "song_9033_part"])
for song_in_query in song_part_list:
        print("\tDownloading assets for: "+song_in_query+"...")
        query=db.execute("select name,hash,size from manifests where name like 'l/"+song_in_query+"/%.awb'")
        part=version+"/solo/"+song_in_query
        if path.exists(part):
                print("")
        else:
                os.makedirs(part)
        fp1=open(version+"\\solo\\"+ song_in_query + "\\p_ren1.bat",'w')
        fp2=open(version+"\\solo\\"+ song_in_query + "\\p_ren2.bat",'w')
        f=Path(cgss_logs+"\\"+song_in_query+".txt")
        f.touch(exist_ok=True)
        f=open(f, 'a')
        f.write("---------------"+str(today)+"---------------\n")
        f.write("Current Manifest Version: "+str(version)+"\n")
        f.close()
        for name,hash,size in query:
                fp1.write("ren "+hash+' '+name[17:]+'\n')
                fp2.write("ren "+name[17:]+' '+hash+'\n')
                if not os.path.exists(version+"\\solo\\"+ song_in_query + "\\"+hash):
                        if verbose:
                                f=Path(cgss_logs+"\\"+song_in_query+".txt")
                                f.touch(exist_ok=True)
                                f=open(f, 'a')
                                f.write(name[2:]+" | "+hash+" | "+humansize(size)+"\n")
                                f.close()
                        url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                        dlfilefrmurl(url,version+"\\solo\\"+song_in_query+"\\"+hash,dl_headers)
                else:
                        if md5chk:
                                with open("\\solo\\"+ song_in_query + "\\"+hash,'rb') as fp:
                                        buf=fp.read()
                                        fp.close()
                                        md5res=hashlib.md5(buf).hexdigest()
                                        del(buf)
                                if md5res!=hash:
                                        if verbose:
                                                print("\tFile "+hash+'('+name+')'+" didn't pass md5check, delete and re-downloading ...")
                                        url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
                                        dlfilefrmurl(url,version+"\\solo\\"+ song_in_query + "\\"+hash,dl_headers)
                                elif verbose:
                                        print("\tFile "+hash+'('+name+')'+" already exists")
        fp1.close()
        fp2.close()
        f=Path(cgss_logs+"\\"+song_in_query+".txt")
        f.touch(exist_ok=True)
        f=open(f, 'a')
        f.write("----------------------------------------\n")
        f.close()
        
print("\tCopying python file for next process ...")
try:
        shutil.copy("bak.py", version)
except OSError:
        print("\tBackup script not found!")
        sys.exit()
sys.exit()
