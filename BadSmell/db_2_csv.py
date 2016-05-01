#!/usr/bin/env python

import os
import csv
import sqlite3


def convert_2_csv(filename,indir,outdir):
    groupName = filename.split('.db')[0]
    print groupName
    conn = sqlite3.connect(indir+filename)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [term[0] for term in cursor]
    conn.text_factory = str
    for table in tables:
        print table
        cursor.execute("SELECT * FROM " + table + ";")
        outfile = groupName+'-'+table+'.csv'
        with open(outdir+outfile, 'wb') as fout:
            cw = csv.writer(fout)
            try:
                cw.writerow([i[0] for i in cursor.description])
                cw.writerows(cursor)
            except Exception as e:
                print(e)
                pass


def main(indir,outdir):
    for fn in os.listdir(indir):
        if (not os.path.isdir(fn)) and ('.db' in fn):
            convert_2_csv(fn,indir,outdir)



if __name__ == "__main__":
    main('./dataCollectionInDB_early/','./dataCollectionInCSV_early/')
    #main('./dataCollectionInDB_last/','./dataCollectionInCSV_last/')