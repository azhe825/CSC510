import os
import csv
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np

indir = "../../dataCollectionInCSV_new/"

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
            m_id = int(row['id'])
            cr_time = row['created_at']
            cl_time = row['closed_at']
            d_time = row['due_at']
            create_time[m_id] = float(cr_time)
            close_time[m_id] = float(cl_time)
            due_time[m_id] = float(d_time)
            sorted(create_time.items())
            sorted(close_time.items())
            sorted(due_time.items())
    group_milestone[group] = (int(groupid), create_time, due_time, close_time)


def main():
    for fn in os.listdir(indir):
        if not os.path.isdir(fn) and ('milestone' in fn) and ('.csv' in fn):
            milestone_time(fn)
    groups = sorted(group_milestone.keys(), key=lambda x: group_milestone[x][0])
    with open("group_milestone_create_time.csv", "wb") as fout:
        cw = csv.writer(fout)
        for gp in groups:
            ids = ['groups']
            ids.extend(group_milestone[gp][1].keys())
            val = [gp.split("group")[1]]
            val.extend(group_milestone[gp][1].values())
            cw.writerow(ids)
            cw.writerow(val)
    with open("group_milestone_close_time.csv", "wb") as fout:
        cw = csv.writer(fout)
        for gp in groups:
            ids = ['groups']
            ids.extend(group_milestone[gp][3].keys())
            val = [gp.split("group")[1]]
            val.extend(group_milestone[gp][3].values())
            cw.writerow(ids)
            cw.writerow(val)
    with open("group_milestone_due_time.csv", "wb") as fout:
        cw = csv.writer(fout)
        for gp in groups:
            ids = ['groups']
            ids.extend(group_milestone[gp][2].keys())
            val = [gp.split("group")[1]]
            val.extend(group_milestone[gp][2].values())
            cw.writerow(ids)
            cw.writerow(val)
    # make bar plot for each group
    for gp in groups:
        print gp
        create_times = np.array(group_milestone[gp][1].values())
        due_times = np.array(group_milestone[gp][2].values())
        closed_times = np.array(group_milestone[gp][3].values())
        size = len(create_times)
        def time_interval(t_delta):
            return (datetime.timedelta(seconds=(t_delta))).days
        due_days = map(time_interval, list(np.subtract(due_times, create_times)))
        closed_days = map(time_interval, list(np.subtract(closed_times, create_times)))
        fig = plt.figure()
        bar_width = 0.4
        opacity = 0.6
        index = np.arange(size)
        barA = plt.bar(index, due_days, bar_width, color='r', alpha=opacity, label='Due')
        barB = plt.bar(index+bar_width, closed_days, bar_width, color='orange', alpha=opacity, label='Closed')
        plt.legend()
        fig.savefig(gp+"-progress.png")


if __name__ == "__main__":
    main()