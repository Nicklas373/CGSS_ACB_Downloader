#!py -3
#!/usr/bin/env python

import csv
import numpy as np
import pandas as pd
import os,sys, os.path
import sqlite3,hashlib
import tabula
from datetime import date
from os import path
from pathlib import Path

cgss_path=os.getcwd()
cgss_logs=cgss_path+"\\logs"
csv_header= ['manifest_music_name', 'music_data_name', 'manifest_version', 'date']
csv_music_data=cgss_logs+"\\music_data\\music_data.csv"
music_data_another=".\\local_data\\music_data_another.db"
music_data=".\\local_data\\music_data.db"
chara_data=".\\local_data\\chara_data.db"
old_files = ["\\sound\\s_ren1.bat","\\sound\\s_ren2.bat","\\txt\\song_1001_vocal_list.txt","\\txt\\song_another_name_list.txt",
                "\\txt\\song_call_name_list.txt","\\txt\\song_collab_name_list.txt","\\txt\\song_movie_name_list.txt","\\txt\\song_se_name_list.txt"]

if not os.path.exists(cgss_path+"\\Static_version"):
        print("\tStatic version are not found !")
        print("\tPlease run cgss.py to get manifests version")
        sys.exit(1)
elif os.path.exists(cgss_path+"\\Static_version"):
        f=Path("Static_version")
        f=open(f)
        version = f.read()
        f.close()
        if version == None:
                print("\tCurrent manifest version = "+version)
                print("\tPlease run cgss.py if you want to get latest manifest version!")

manifests=".\\manifests\\manifest_"+version+".db"
manifests_con=sqlite3.Connection(manifests)
music_data_con=sqlite3.Connection(music_data)
music_data_another_con=sqlite3.Connection(music_data_another)
today=date.today()
vocal_data_con=sqlite3.Connection(chara_data)
xlsx_music_data=cgss_logs+"\\music_data\\music_data.xlsx"

print("\tCGSS ACB Auto Renamer | Starting!")
print("\tUpdate & Maintain by @Nicklas373")
print("\tCleanup old log from rename file is exists! ...")

for old_log in old_files:
        if old_log == "\\sound\\s_ren1.bat" or old_log == "\\sound\\s_ren2.bat":
                if not os.path.exists(cgss_path+"\\"+version+old_log):
                        os.remove(cgss_path+"\\"+version+old_log)
        else:
                if not os.path.exists(cgss_logs+old_log):
                        os.remove(cgss_logs+old_log)
        
solo_list = np.loadtxt(cgss_logs+"\\txt\\solo_list.txt", dtype=str, delimiter=",")
for solo_in_query in solo_list:
        if os.path.exists(cgss_logs+"\\txt\\"+str(solo_in_query)+"_vocal.txt"):
                os.remove(cgss_logs+"\\txt\\"+str(solo_in_query)+"_vocal.txt")
                
        if os.path.exists(version+"\\solo\\"+solo_in_query+"\\sva_ren1.bat"):
                os.remove(version+"\\solo\\"+solo_in_query+"\\sva_ren1.bat")
                
        if os.path.exists(version+"\\solo\\"+solo_in_query+"\\sva_ren2.bat"):
                os.remove(version+"\\solo\\"+solo_in_query+"\\sva_ren2.bat")
        
print("\tBegin generate music name list from database...")
print("\tCreate name list for "+version+"/sound in database from manifests ...\n")
query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song%.acb' and size > '7000' and name not like 'l/song_%_another.acb' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_se.acb' and name not like 'l/song_%_movie.acb'")
for name,hash,size in query:
    f=open(cgss_logs+"\\txt\\song_main_name_list.txt", 'a')
    if (int(name[7:][:-4]) > 1000):
            f.write(name[7:][:-4]+"\n")
    else:
            print("")
    f.close()

if os.path.exists(csv_music_data):
        print("\tCleanup old music data (CSV)..")
        os.remove(csv_music_data)

if os.path.exists(xlsx_music_data):
        print("\tCleanup old music data (XLSX)..")
        os.remove(xlsx_music_data)

song_main_name_list = np.loadtxt(cgss_logs+"\\txt\\"+"song_main_name_list.txt", dtype=str, delimiter=",")
for song_main_name in song_main_name_list:
    query=music_data_con.execute("select id, name from music_data where id like '"+song_main_name+"'")
    if not os.path.exists(csv_music_data):
                f = open(csv_music_data, 'w', encoding='UTF8', newline='')
                writer = csv.writer(f)
                writer.writerow(csv_header)
                f.close() 
    for id,name in query:
                fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
                fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
                replace_phase_1 = str(name).replace(' ','_')
                replace_phase_2 = str(replace_phase_1).replace('\n','')
                fp1.write("ren song_"+str(id)+".hca"+ ' '+str(replace_phase_2).replace("\n"," ")+".hca"+"\n")
                fp2.write("ren "+str(replace_phase_2).replace('/n','')+".hca"+' '+"song_"+str(id)+".hca"+"\n")
                fp1.close()
                fp2.close()
                csv_solo_rows=["song_"+str(id)+".hca", str(replace_phase_2).replace("\n"," ")+".hca", version, today.strftime("%d/%m/%Y")]
                f = open(csv_music_data, 'a', encoding='UTF8', newline='')
                writer = csv.writer(f)
                writer.writerow(csv_solo_rows)
                f.close()

print("\tCreate auto rename for "+version+"/sound_another in database from manifests ...\n")
query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_%_another.acb' and size > '7000' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_se.acb' and name not like 'l/song_%_movie.acb'")
for name,hash,size in query:
    f=open(cgss_logs+"\\txt\\song_another_name_list.txt", 'a')
    f.write(name[7:][:-4]+"\n")
    f.close()

song_another_name_list = np.loadtxt(cgss_logs+"\\txt\\"+"song_another_name_list.txt", dtype=str, delimiter=",")
for song_another_name in song_another_name_list:
    query=music_data_another_con.execute("select music_id, name from music_another_data where music_id like '"+song_another_name+"'")
    for music_id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_"+music_id+".hca"+ ' '+str(name).replace(' ','_')+"_another.hca"+"\n")
        fp2.write("ren "+str(name).replace(' ','_')+"_another.hca"+' '+"song_"+music_id+".hca"+"\n")
        fp1.close()
        fp2.close()
        csv_solo_rows=["song_"+str(music_id)+".hca", str(name).replace(' ','_')+"_another.hca", version, today.strftime("%d/%m/%Y")]
        f = open(csv_music_data, 'a', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerow(csv_solo_rows)
        f.close()

print("\tCreate auto rename for "+version+"/sound_call in database from manifests ...\n")
query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_%_call.acb' and size > '7000' and name not like 'l/song_%_another.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_se.acb' and name not like 'l/song_%_movie.acb'")
for name,hash,size in query:
    f=open(cgss_logs+"\\txt\\song_call_name_list.txt", 'a')
    f.write(name[7:][:-4]+"\n")
    f.close()

song_call_name_list = np.loadtxt(cgss_logs+"\\txt\\"+"song_call_name_list.txt", dtype=str, delimiter=",")
for song_call_name in song_call_name_list:
    query=music_data_another_con.execute("select music_id, name from music_another_data where music_id like '"+song_call_name+"'")
    for music_id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_"+music_id+".hca"+ ' '+str(name).replace(' ','_')+"_call.hca"+"\n")
        fp2.write("ren "+str(name).replace(' ','_')+"_call.hca"+' '+"song_"+music_id+".hca"+"\n")
        fp1.close()
        fp2.close()
        csv_solo_rows=["song_"+str(music_id)+".hca", str(name).replace(' ','_')+"_call.hca", version, today.strftime("%d/%m/%Y")]
        f = open(csv_music_data, 'a', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerow(csv_solo_rows)
        f.close()

query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_%_collab.acb' and size > '7000' and name not like 'l/song_%_another.acb' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_se.acb' and name not like 'l/song_%_movie.acb'")
print("\tCreate auto rename for "+version+"/sound_collab in database from manifests ...\n")
for name,hash,size in query:
    f=open(cgss_logs+"\\txt\\song_collab_name_list.txt", 'a')
    f.write(name[7:][:-4]+"\n")
    f.close()

song_collab_name_read = open(cgss_logs+"\\txt\\"+"song_collab_name_list.txt", "r")
song_collab_name = song_collab_name_read.read()
query=music_data_con.execute("select id, name from music_data where id like '"+song_collab_name[:-8]+"'")
for id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_"+str(id)+".hca"+ ' '+str(name).replace(' ','_')+"_collab.hca"+"\n")
        fp2.write("ren "+str(name).replace(' ','_')+"_collab.hca"+' '+"song_"+str(id)+".hca"+"\n")
        fp1.close()
        fp2.close()
        csv_solo_rows=["song_"+str(id)+".hca", str(name).replace(' ','_')+"_collab.hca", version, today.strftime("%d/%m/%Y")]
        f = open(csv_music_data, 'a', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerow(csv_solo_rows)
        f.close()

query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_%_se.acb' and size > '7000' and name not like 'l/song_%_another.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_movie.acb'")
print("\tCreate auto rename for "+version+"/sound_se in database from manifests ...\n")
for name,hash,size in query:
    f=open(cgss_logs+"\\txt\\song_se_name_list.txt", 'a')
    f.write(name[7:][:-4]+"\n")
    f.close()

song_se_name_list = np.loadtxt(cgss_logs+"\\txt\\"+"song_se_name_list.txt", dtype=str, delimiter=",")
for song_se_name in song_se_name_list:
    query=music_data_con.execute("select id, name from music_data where id like '"+song_se_name[:-3]+"'")
    for id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_"+str(id)+".hca"+ ' '+str(name).replace(' ','_')+"_se.hca"+"\n")
        fp2.write("ren "+str(name).replace(' ','_')+"_se.hca"+' '+"song_"+str(id)+".hca"+"\n")
        fp1.close()
        fp2.close()
        csv_solo_rows=["song_"+str(id)+".hca", str(name).replace(' ','_')+"_se.hca", version, today.strftime("%d/%m/%Y")]
        f = open(csv_music_data, 'a', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerow(csv_solo_rows)
        f.close()

query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_%_movie.acb' and size > '7000' and name not like 'l/song_%_another.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_se.acb'")
print("\tCreate auto rename for "+version+"/sound_movie in database from manifests ...\n")
for name,hash,size in query:
    f=open(cgss_logs+"\\txt\\song_movie_name_list.txt", 'a')
    f.write(name[7:][:-4]+"\n")
    f.close()

song_movie_name_read = open(cgss_logs+"\\txt\\"+"song_movie_name_list.txt", "r")
song_movie_name_list = song_movie_name_read.read()
query=music_data_con.execute("select id, name from music_data where id like '"+song_movie_name_list[:-7]+"'")
for id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_"+str(id)+".hca"+ ' '+str(name).replace(' ','_')+"_movie.hca"+"\n")
        fp2.write("ren "+str(name).replace(' ','_')+"_movie.hca"+' '+"song_"+str(id)+".hca"+"\n")
        fp1.close()
        fp2.close()
        csv_solo_rows=["song_"+str(id)+".hca", str(name).replace(' ','_')+"movie.hca", version, today.strftime("%d/%m/%Y")]
        f = open(csv_music_data, 'a', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerow(csv_solo_rows)
        f.close()
        
print("\tCreate auto rename for "+version+"/sound_1001 in database from manifests ...\n")
query=manifests_con.execute("select name,hash,size from manifests where name like 'l/song_1001_%.acb' and size > '7000' and name not like 'l/song_%_call.acb' and name not like 'l/song_%_collab.acb' and name not like 'l/song_%_se.acb' and name not like 'l/song_%_movie.acb'")
for name,hash,size in query:
    f=open(cgss_logs+"\\txt\\song_1001_vocal_list.txt", 'a')
    f.write(name[12:][:-4]+"\n")
    f.close()

song_1001_vocal_list = np.loadtxt(cgss_logs+"\\txt\\"+"song_1001_vocal_list.txt", dtype=str, delimiter=",")
for song_1001_vocal in song_1001_vocal_list:
    query=vocal_data_con.execute("select chara_id, name from chara_data where chara_id like '"+song_1001_vocal+"'")
    for chara_id,name in query:
        fp1=open(version+"\\sound\\s_ren1.bat", 'a', encoding='utf8')
        fp2=open(version+"\\sound\\s_ren2.bat", 'a', encoding='utf8')
        fp1.write("ren song_1001_"+str(chara_id)+".hca"+ ' お願い_!_シンデレラ~'+str(name).replace(' ','_')+".hca"+"\n")
        fp2.write("ren お願い_!_シンデレラ~"+str(name).replace(' ','_')+".hca"+' '+"song_1001_"+str(chara_id)+".hca"+"\n")
        fp1.close()
        fp2.close()
        csv_solo_rows=["song_1001_"+str(chara_id)+".hca", ' お願い_!_シンデレラ~'+str(name).replace(' ','_')+".hca", version, today.strftime("%d/%m/%Y")]
        f = open(csv_music_data, 'a', encoding='UTF8', newline='')
        writer = csv.writer(f)
        writer.writerow(csv_solo_rows)
        f.close()

print("\tCreate auto rename for "+version+"/sound_solo_part in database from manifests ...\n")
solo_list = np.loadtxt(cgss_logs+"\\txt\\solo_list.txt", dtype=str, delimiter=",")
for solo_in_query in solo_list:
        query = manifests_con.execute("select name, hash, size from manifests where name like 'l/"+solo_in_query+"/vo_solo_%_0%.awb'")
        f=open(cgss_logs+"\\txt\\"+solo_in_query+"_vocal.txt", 'a')
        for name, hash, size in query:
                f.write(str(name[31:][:-4])+"\n")
        f.close()

solo_list = np.loadtxt(cgss_logs+"\\txt\\solo_list.txt", dtype=str, delimiter=",")
for solo_in_query in solo_list:
        sub_solo_list = np.loadtxt(cgss_logs+"\\txt\\"+solo_in_query+"_vocal.txt", dtype=str, delimiter=",")
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
                                csv_solo_rows=["vo_solo_"+solo_id_trim_2+"_0"+str(trim_sub_solo_2)+".awb", str(music_name.replace('\n',"_"))+"~"+str(trim_sub_chara_2)+".awb", version, today.strftime("%d/%m/%Y")]
                                f = open(csv_music_data, 'a', encoding='UTF8', newline='')
                                writer = csv.writer(f)
                                writer.writerow(csv_solo_rows)
                                f.close()


solo_list = np.loadtxt(cgss_logs+"\\txt\\solo_list.txt", dtype=str, delimiter=",")
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
                csv_solo_rows=["inst_song_"+solo_id_trim_2+".awb", "inst_"+str(music_name).replace(" ","_")+".awb", version, today.strftime("%d/%m/%Y")]
                f = open(csv_music_data, 'a', encoding='UTF8', newline='')
                writer = csv.writer(f)
                writer.writerow(csv_solo_rows)
                f.close()

print("\tDump music data into XLSX!")
read_file = pd.read_csv(csv_music_data, on_bad_lines='skip')
read_file.to_excel(xlsx_music_data, index=None, header=True)

if os.path.isfile(xlsx_music_data):
        print("\tDump success...")
        print("\tCheck music data on logs/music_data/music_data.xlsx...")
else:
        print("\tDump failed...")
        print("\tCheck music data on logs/music_data/music_data.csv...")

print("\tCGSS ACB Renamer List | Finished!")      
