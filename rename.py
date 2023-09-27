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
import csv
from csv import writer, reader

version=None

if not version:
        f=Path("Static_version")
        f=open(f)
        version = f.read()
        f.close()
        print("\tCurrent manifest version = "+version)
        print("\tPlease run cgss.py if you want to get latest manifest version!")

def implementNewColandRow(inputcsv,outputcsv,newheader,newrow):
        reader = csv.reader(open(inputcsv, 'r', encoding='UTF8', newline=''))
        writer = csv.writer(open(outputcsv, 'w', encoding='UTF8', newline=''))
        headers = next(reader)
        headers.append(newheader)
        writer.writerow(headers)
        for row in reader:
            row.append(newrow)
            writer.writerow(row)
            
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

if path.exists(cgss_logs+"\\rename"):
    print("")
else:
    os.makedirs(cgss_logs+"\\rename\\")
        
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
        default_text = str(name)
        # Open the input_file in read mode and output_file in write mode
        with open(cgss_logs+'\\sound.csv', 'r', encoding='UTF8') as read_obj, \
                open('output_1.csv', 'w', newline='', encoding='UTF8') as write_obj:
            # Create a csv.reader object from the input file object
            csv_reader = reader(read_obj)
            # Create a csv.writer object from the output file object
            csv_writer = writer(write_obj)
            # Read each row of the input csv file as list
            for row in csv_reader:
                    for id,name in query:
                        # Append the default text in the row / list
                        row.append(str(name))
                        # Add the updated row / list to the output file
                        csv_writer.writerow(row)
            
print("\tCGSS ACB Renamer List | Finished!")      
