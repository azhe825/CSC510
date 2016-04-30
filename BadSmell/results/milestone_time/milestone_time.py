import os
import csv
import time
import datetime
import matplotlib.pyplot as plt

indir = "../../dataCollectionInCSV/"

tJan = datetime.datetime(year=2016, month=1, day=7) # time for January
tFeb = datetime.datetime(year=2016, month=2, day=1)
tMar = datetime.datetime(year=2016, month=3, day=1)
tApr = datetime.datetime(year=2016, month=4, day=1)
tMay = datetime.datetime(year=2016, month=5, day=1)
tStart = time.mktime(tJan.timetuple()) # start of this project

group_milestone = dict()

def milestone_time(filename):
    group = filename.split('-')[0]
    groupid = group.split('group')[1]
    create_time = dict()
    close_time = dict()
    due_time = dict()
    with open(indir+filename, 'rb') as fin:
        cr = csv.DictReader(fin)
        for row in cr:
            m_id = row['id']
            cr_time = row['created_at']
            cl_time = row['closed_at']
            d_time = row['due_at']
            create_time[m_id] = int(cr_time)
            close_time[m_id] = int(cl_time)
            due_time[m_id] = int(d_time)







def main():
    for fn in os.listdir(indir):
        if not os.path.isdir(fn) and ('milestone' in fn) and ('.csv' in fn):
            milestone_time(fn)



if __name__ == "__main__":
    main()