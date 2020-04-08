#!py -3
#!/usr/bin/env python

def usage():
	print("\tUsage:run.py [-v <VERSION>] [-g] [-s] [-m]")
	return

import os,sys
import requests
import json
import sqlite3,hashlib
from lz4 import block
import time
import shutil

def dlfilefrmurl(url,path,headers):
	r=requests.get(url,headers=headers)
	fp=open(path,'wb')
	if verbose:
		print("\tWriting into disk ...")
	fp.write(r.content)
	fp.close()
	ldate=r.headers['Last-Modified']
	timeStruct=time.strptime(ldate,"%a, %d %b %Y %H:%M:%S GMT")
	timestamp=time.mktime(timeStruct)+8*60*60
	os.utime(path,(os.stat(path).st_atime,timestamp))
	r.close()

version=None
gennamelist=False
verbose=True
md5chk=False
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
                        print("\tGetting game version ...")
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
	print("\tGame Version = "+version)
if not os.path.exists(".\\"+version):
	os.mkdir(version)

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
query=db.execute("select name,hash from manifests where name like 'b/%.acb'")
bgm=version+"/bgm"
if os.path.isdir(version+"\\bgm\\"):
    print("")
else:
    os.makedirs(bgm)
fp1=open(version+"\\bgm\\b_ren1.bat",'w')
fp2=open(version+"\\bgm\\b_ren2.bat",'w')
for name,hash in query:
	fp1.write("ren "+hash+' '+name[2:]+'\n')
	fp2.write("ren "+name[2:]+' '+hash+'\n')
	if not os.path.exists(version+"\\bgm\\"+hash):
		if verbose:
			print("\tDownloading file "+hash+'('+name+')')
		url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
		dlfilefrmurl(url,version+"\\bgm\\"+hash,dl_headers)
	else:
		if md5chk:
			with open("\\bgm\\"+hash,'rb') as fp:
				buf=fp.read()
				fp.close()
				md5res=hashlib.md5(buf).hexdigest()
				del(buf)
			if md5res!=hash:
				if verbose:
					print("\tFile "+hash+'('+name+')'+" didn't pass md5check, delete and re-downloading ...")
				url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
				dlfilefrmurl(url,version+"\\bgm\\"+hash,dl_headers)
			elif verbose:
				print("\tFile "+hash+'('+name+')'+" already exists")
		elif verbose:
			print("\tFile "+hash+'('+name+')'+" already exists")
fp1.close()
fp2.close()
query=db.execute("select name,hash from manifests where name like 'l/%.acb'")
sound=version+"/sound"
if os.path.isdir(version+"\\sound\\"):
    print("")
else:
    os.makedirs(sound)
fp1=open(version+"\\sound\\l_ren1.bat",'w')
fp2=open(version+"\\sound\\l_ren2.bat",'w')
for name,hash in query:
	fp1.write("ren "+hash+' '+name[2:]+'\n')
	fp2.write("ren "+name[2:]+' '+hash+'\n')
	if not os.path.exists(version+"\\sound\\"+hash):
		if verbose:
			print("\tDownloading file "+hash+'('+name+')')
		url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
		dlfilefrmurl(url,version+"\\sound\\"+hash,dl_headers)
	else:
		if md5chk:
			with open("\\sound\\"+hash,'rb') as fp:
				buf=fp.read()
				fp.close()
				md5res=hashlib.md5(buf).hexdigest()
				del(buf)
			if md5res!=hash:
				if verbose:
					print("\tFile "+hash+'('+name+')'+" didn't pass md5check, delete and re-downloading ...")
				url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
				dlfilefrmurl(url,version+"\\sound\\"+hash,dl_headers)
			elif verbose:
				print("\tFile "+hash+'('+name+')'+" already exists")
		elif verbose:
			print("\tFile "+hash+'('+name+')'+" already exists")
fp1.close()
fp2.close()
query=db.execute("select name,hash from manifests where name like 'l/%.awb'")
solo=version+"/solo"
if os.path.isdir(version+"\\solo\\"):
    print("")
else:
    os.makedirs(solo)
fp1=open(version+"\\solo\\s_ren1.bat",'w')
fp2=open(version+"\\solo\\s_ren2.bat",'w')
for name,hash in query:
	fp1.write("ren "+hash+' '+name[17:]+'\n')
	fp2.write("ren "+name[17:]+' '+hash+'\n')
	if not os.path.exists(version+"\\solo\\"+hash):
		if verbose:
			print("\tDownloading file "+hash+'('+name+')')
		url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
		dlfilefrmurl(url,version+"\\solo\\"+hash,dl_headers)
	else:
		if md5chk:
			with open("\\solo\\"+hash,'rb') as fp:
				buf=fp.read()
				fp.close()
				md5res=hashlib.md5(buf).hexdigest()
				del(buf)
			if md5res!=hash:
				if verbose:
					print("\tFile "+hash+'('+name+')'+" didn't pass md5check, delete and re-downloading ...")
				url="http://asset-starlight-stage.akamaized.net/dl/resources/Sound/"+hash[:2]+"/"+hash
				dlfilefrmurl(url,version+"\\solo\\"+hash,dl_headers)
			elif verbose:
				print("\tFile "+hash+'('+name+')'+" already exists")
		elif verbose:
			print("\tFile "+hash+'('+name+')'+" already exists")
fp1.close()
fp2.close()
db.close()
if verbose:
	print("\tFinished analysing database ...")

print("\tCopying python file for next process ...")
shutil.copy("bak.py", version)
