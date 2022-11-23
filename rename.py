#!py -3
#!/usr/bin/env python

def usage():
	print("\tUsage:rename.py")
	return

import os,sys, os.path
from os import path
from pathlib import Path
import sqlite3,hashlib
import numpy as np

version=None

if not version:
        f=Path("Static_version")
        f=open(f)
        version = f.read()
        f.close()
        print("\tCurrent manifest version = "+version)
        print("\tPlease run cgss.py if you want to get latest manifest version!")

cgss_path=os.getcwd()
cgss_logs=cgss_path+"\\logs"
manifests=".\\manifests\\manifest_"+version+".db"
music_data_another=".\\local_data\\music_data_another.db"
music_data=".\\local_data\\music_data.db"
chara_data=".\\local_data\\chara_data.db"
manifests_con=sqlite3.Connection(manifests)
music_data_con=sqlite3.Connection(music_data)
music_data_another_con=sqlite3.Connection(music_data_another)
vocal_data_con=sqlite3.Connection(chara_data)

print("\tCGSS ACB Auto Renamer | Starting!")
print("\tUpdate & Maintain by @Nicklas373")
print("\tCleanup old log from rename file is exists! ...")
if os.path.isfile(version+"\\sound\\s_ren1.bat"):
        os.remove(version+"\\sound\\s_ren1.bat")
else:
        print("")

if os.path.isfile(version+"\\sound\\s_ren2.bat"):
        os.remove(version+"\\sound\\s_ren2.bat")
else:
        print("")

if os.path.isfile(cgss_logs+"\\rename\\song_1001_vocal_list.txt"):
        os.remove(cgss_logs+"\\rename\\song_1001_vocal_list.txt")
else:
        print("")
        
if os.path.isfile(cgss_logs+"\\rename\\song_main_name_list.txt"):
        os.remove(cgss_logs+"\\rename\\song_main_name_list.txt")
else:
        print("")
        
if os.path.isfile(cgss_logs+"\\rename\\song_another_name_list.txt"):
        os.remove(cgss_logs+"\\rename\\song_another_name_list.txt")
else:
        print("")

if os.path.isfile(cgss_logs+"\\rename\\song_call_name_list.txt"):
        os.remove(cgss_logs+"\\rename\\song_call_name_list.txt")
else:
        print("")

if os.path.isfile(cgss_logs+"\\rename\\song_collab_name_list.txt"):
        os.remove(cgss_logs+"\\rename\\song_collab_name_list.txt")
else:
        print("")

if os.path.isfile(cgss_logs+"\\rename\\song_movie_name_list.txt"):
        os.remove(cgss_logs+"\\rename\\song_movie_name_list.txt")
else:
        print("")

if os.path.isfile(cgss_logs+"\\rename\\song_se_name_list.txt"):
        os.remove(cgss_logs+"\\rename\\song_se_name_list.txt")
else:
        print("")
        
solo_list = np.loadtxt(cgss_logs+"\\solo_list.txt", dtype=str, delimiter=",")
for solo_in_query in solo_list:
        if os.path.isfile(cgss_logs+"\\rename\\"+str(solo_in_query)+"_vocal.txt"):
                os.remove(cgss_logs+"\\rename\\"+str(solo_in_query)+"_vocal.txt")
        else:
                print("")
                
        if os.path.isfile(version+"\\solo\\"+solo_in_query+"\\sva_ren1.bat"):
                os.remove(version+"\\solo\\"+solo_in_query+"\\sva_ren1.bat")
        else:
                print("")
                
        if os.path.isfile(version+"\\solo\\"+solo_in_query+"\\sva_ren2.bat"):
                os.remove(version+"\\solo\\"+solo_in_query+"\\sva_ren2.bat")
        else:
                print("")
        
print("\tBegin generate music name list from database...")
print("\tCreate name list for "+version+"/sound in database from manifests ...\n")
query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song%.acb' and size > '7000' and name not like 'l/song_%_another.acb' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_se.acb' and name not like 'l/song_%_movie.acb'")
for name,hash,size in query:
    f=open(cgss_logs+"\\rename\\song_main_name_list.txt", 'a')
    if (int(name[7:][:-4]) > 1000):
            f.write(name[7:][:-4]+"\n")
    else:
            print("")
    f.close()

song_main_name_list = np.loadtxt(cgss_logs+"\\rename\\"+"song_main_name_list.txt", dtype=str, delimiter=",")
for song_main_name in song_main_name_list:
    query=music_data_con.execute("select id, name from music_data where id like '"+song_main_name+"'")
    for id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        replace_phase_1 = str(name).replace(' ','_')
        replace_phase_2 = str(replace_phase_1).replace('\n','')
        fp1.write("ren song_"+str(id)+".hca"+ ' '+str(replace_phase_2).replace("\n"," ")+".hca"+"\n")
        fp2.write("ren "+str(replace_phase_2).replace('/n','')+".hca"+' '+"song_"+str(id)+".hca"+"\n")
        fp1.close()
        fp2.close()

print("\tCreate auto rename for "+version+"/sound_another in database from manifests ...\n")
query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_%_another.acb' and size > '7000' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_se.acb' and name not like 'l/song_%_movie.acb'")
for name,hash,size in query:
    f=open(cgss_logs+"\\rename\\song_another_name_list.txt", 'a')
    f.write(name[7:][:-4]+"\n")
    f.close()

song_another_name_list = np.loadtxt(cgss_logs+"\\rename\\"+"song_another_name_list.txt", dtype=str, delimiter=",")
for song_another_name in song_another_name_list:
    query=music_data_another_con.execute("select music_id, name from music_another_data where music_id like '"+song_another_name+"'")
    for music_id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_"+music_id+".hca"+ ' '+str(name).replace(' ','_')+"_another.hca"+"\n")
        fp2.write("ren "+str(name).replace(' ','_')+"_another.hca"+' '+"song_"+music_id+".hca"+"\n")
        fp1.close()
        fp2.close()

print("\tCreate auto rename for "+version+"/sound_call in database from manifests ...\n")
query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_%_call.acb' and size > '7000' and name not like 'l/song_%_another.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_se.acb' and name not like 'l/song_%_movie.acb'")
for name,hash,size in query:
    f=open(cgss_logs+"\\rename\\song_call_name_list.txt", 'a')
    f.write(name[7:][:-4]+"\n")
    f.close()

song_call_name_list = np.loadtxt(cgss_logs+"\\rename\\"+"song_call_name_list.txt", dtype=str, delimiter=",")
for song_call_name in song_call_name_list:
    query=music_data_another_con.execute("select music_id, name from music_another_data where music_id like '"+song_call_name+"'")
    for music_id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_"+music_id+".hca"+ ' '+str(name).replace(' ','_')+"_call.hca"+"\n")
        fp2.write("ren "+str(name).replace(' ','_')+"_call.hca"+' '+"song_"+music_id+".hca"+"\n")
        fp1.close()
        fp2.close()

query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_%_collab.acb' and size > '7000' and name not like 'l/song_%_another.acb' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_se.acb' and name not like 'l/song_%_movie.acb'")
print("\tCreate auto rename for "+version+"/sound_collab in database from manifests ...\n")
for name,hash,size in query:
    f=open(cgss_logs+"\\rename\\song_collab_name_list.txt", 'a')
    f.write(name[7:][:-4]+"\n")
    f.close()

song_collab_name_read = open(cgss_logs+"\\rename\\"+"song_collab_name_list.txt", "r")
song_collab_name = song_collab_name_read.read()
query=music_data_con.execute("select id, name from music_data where id like '"+song_collab_name[:-8]+"'")
for id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_"+str(id)+".hca"+ ' '+str(name).replace(' ','_')+"_collab.hca"+"\n")
        fp2.write("ren "+str(name).replace(' ','_')+"_collab.hca"+' '+"song_"+str(id)+".hca"+"\n")
        fp1.close()
        fp2.close()

query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_%_se.acb' and size > '7000' and name not like 'l/song_%_another.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_movie.acb'")
print("\tCreate auto rename for "+version+"/sound_se in database from manifests ...\n")
for name,hash,size in query:
    f=open(cgss_logs+"\\rename\\song_se_name_list.txt", 'a')
    f.write(name[7:][:-4]+"\n")
    f.close()

song_se_name_list = np.loadtxt(cgss_logs+"\\rename\\"+"song_se_name_list.txt", dtype=str, delimiter=",")
for song_se_name in song_se_name_list:
    query=music_data_con.execute("select id, name from music_data where id like '"+song_se_name[:-3]+"'")
    for id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_"+str(id)+".hca"+ ' '+str(name).replace(' ','_')+"_se.hca"+"\n")
        fp2.write("ren "+str(name).replace(' ','_')+"_se.hca"+' '+"song_"+str(id)+".hca"+"\n")
        fp1.close()
        fp2.close()

query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_%_movie.acb' and size > '7000' and name not like 'l/song_%_another.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_se.acb'")
print("\tCreate auto rename for "+version+"/sound_movie in database from manifests ...\n")
for name,hash,size in query:
    f=open(cgss_logs+"\\rename\\song_movie_name_list.txt", 'a')
    f.write(name[7:][:-4]+"\n")
    f.close()

song_movie_name_read = open(cgss_logs+"\\rename\\"+"song_movie_name_list.txt", "r")
song_movie_name_list = song_movie_name_read.read()
query=music_data_con.execute("select id, name from music_data where id like '"+song_movie_name_list[:-7]+"'")
for id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_"+str(id)+".hca"+ ' '+str(name).replace(' ','_')+"_movie.hca"+"\n")
        fp2.write("ren "+str(name).replace(' ','_')+"_movie.hca"+' '+"song_"+str(id)+".hca"+"\n")
        fp1.close()
        fp2.close()
        
print("\tCreate auto rename for "+version+"/sound_1001 in database from manifests ...\n")
query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_1001_%.acb' and size > '7000' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_se.acb' and name not like 'l/song_%_movie.acb'")
for name,hash,size in query:
    f=open(cgss_logs+"\\rename\\song_1001_vocal_list.txt", 'a')
    f.write(name[12:][:-4]+"\n")
    f.close()

song_1001_vocal_list = np.loadtxt(cgss_logs+"\\rename\\"+"song_1001_vocal_list.txt", dtype=str, delimiter=",")
for song_1001_vocal in song_1001_vocal_list:
    query=vocal_data_con.execute("select chara_id, name from chara_data where chara_id like '"+song_1001_vocal+"'")
    for chara_id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_1001_"+str(chara_id)+".hca"+ ' お願い_!_シンデレラ~'+str(name).replace(' ','_')+".hca"+"\n")
        fp2.write("ren お願い_!_シンデレラ~"+str(name).replace(' ','_')+".hca"+' '+"song_1001_"+str(chara_id)+".hca"+"\n")
        fp1.close()
        fp2.close()

print("\tCreate auto rename for "+version+"/sound_solo_part in database from manifests ...\n")
solo_list = np.loadtxt(cgss_logs+"\\"+"solo_list.txt", dtype=str, delimiter=",")
for solo_in_query in solo_list:
        query = manifests_con.execute("select name, hash, size from manifests where name like 'l/"+solo_in_query+"/vo_solo_%_0%.awb'")
        f=open(cgss_logs+"\\rename\\"+solo_in_query+"_vocal.txt", 'a')
        for name, hash, size in query:
                f.write(str(name[31:][:-4])+"\n")
        f.close()

solo_list = np.loadtxt(cgss_logs+"\\"+"solo_list.txt", dtype=str, delimiter=",")
for solo_in_query in solo_list:
        sub_solo_list = np.loadtxt(cgss_logs+"\\rename\\"+solo_in_query+"_vocal.txt", dtype=str, delimiter=",")
        fp1=open(version+"\\solo\\"+solo_in_query+"\\sva_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\solo\\"+solo_in_query+"\\sva_ren2.bat", 'a', encoding='utf8')
        for sub_solo_list_in_query in sub_solo_list:
                solo_id_trim = solo_in_query[5:][:-5]
                query1 = music_data_con.execute("select id, name as music_name from music_data where id like '"+solo_id_trim+"'")
                for id, music_name in query1:
                        if (sub_solo_list_in_query[3:] == "_1"):
                                trim_sub_solo = sub_solo_list_in_query[:-2]
                        elif (sub_solo_list_in_query[3:] == "_2"):
                                trim_sub_solo = sub_solo_list_in_query[:-2]
                        else:
                                trim_sub_solo = sub_solo_list_in_query
                        query2 = vocal_data_con.execute("select chara_id, name as chara_name from chara_data where chara_id like '"+trim_sub_solo+"'")
                        for chara_id, chara_name in query2:
                                solo_id_trim_2 = solo_in_query[5:][:-5]
                                if (sub_solo_list_in_query[3:] == "_1"):
                                        trim_sub_solo_2 = str(chara_id)+"_1"
                                        trim_sub_chara_2 = str(chara_name)+"_1"
                                elif (sub_solo_list_in_query[3:] == "_2"):
                                        trim_sub_solo_2 = str(chara_id)+"_2"
                                        trim_sub_chara_2 = str(chara_name)+"_2"
                                else:
                                        trim_sub_solo_2 = str(chara_id)
                                        trim_sub_chara_2 = str(chara_name)
                                fp1.write("ren vo_solo_"+solo_id_trim_2+"_0"+str(trim_sub_solo_2)+".awb"+' '+str(music_name.replace('\n',"_"))+"~"+str(trim_sub_chara_2)+".awb"+"\n")
                                fp2.write("ren "+str(music_name.replace('\n',"_"))+"~"+str(trim_sub_chara_2)+".awb"+' '+"vo_solo_"+solo_id_trim_2+"_0"+str(trim_sub_solo_2)+".awb"+"\n")
                                fp1.close
                                fp2.close           


solo_list = np.loadtxt(cgss_logs+"\\"+"solo_list.txt", dtype=str, delimiter=",")
for solo_in_query in solo_list:
        fp1=open(version+"\\solo\\"+solo_in_query+"\\sva_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\solo\\"+solo_in_query+"\\sva_ren2.bat", 'a', encoding='utf8')
        solo_id_trim = solo_in_query[5:][:-5]
        query1 = music_data_con.execute("select id, name as music_name from music_data where id like '"+solo_id_trim+"'")
        for id, music_name in query1:
                solo_id_trim_2 = solo_in_query[5:][:-5]
                fp1.write("ren inst_song_"+solo_id_trim_2+".awb"+' '+"inst_"+str(music_name).replace(" ","_")+".awb"+"\n")
                fp2.write("ren inst_"+str(music_name).replace(" ","_")+".awb"+' '+"inst_song_"+solo_id_trim_2+".awb"+"\n")
        fp1.close
        fp2.close
      
print("\tCGSS ACB Renamer List | Finished!")      