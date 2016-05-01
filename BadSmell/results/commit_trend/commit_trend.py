import csv
import os
import datetime
import time
import matplotlib.pyplot as plt

indir = '../../dataCollectionInCSV_new/'
outdir = './'
group_commits = dict()

tJan = datetime.datetime(year=2016, month=1, day=7) # time for January
tFeb = datetime.datetime(year=2016, month=2, day=1)
tMar = datetime.datetime(year=2016, month=3, day=1)
tApr = datetime.datetime(year=2016, month=4, day=1)
tMay = datetime.datetime(year=2016, month=5, day=1)
tStart = time.mktime(tJan.timetuple()) # start of this project

def commit_trend(filename):
    commit_vs_days = dict()
    totalDays = int((tMay - tJan).days)
    for i in range(totalDays):
        commit_vs_days.update({i+1 : 0})
    group = filename.split('-commits')[0]
    groupid = group.split('group')[1]
    #print groupid
    with open(indir+filename, 'rb') as fin:
        cr = csv.DictReader(fin)
        for row in cr:
            cur_time = int(row["time"])
            duration = datetime.timedelta(seconds=(cur_time - tStart)).days
            if commit_vs_days.has_key(duration):
                commit_vs_days[duration] += 1
    commit_sum = [0 for _ in range(totalDays+1)]
    for i in range(totalDays):
        num_of_commits = commit_sum[i] + commit_vs_days[i+1]
        commit_sum[i+1] = num_of_commits
    group_commits[group] = (int(groupid), commit_sum)


def main():
    for fn in os.listdir(indir):
        if (not os.path.isdir(fn)) and fn.__contains__('.csv') and fn.__contains__('-commits'):
            commit_trend(fn)
    groups = sorted(group_commits.keys(), key=lambda x: group_commits[x][0])
    totalDays = int((tMay - tJan).days)
    deadlineFeb = int((tFeb - tJan).days)
    deadlineMar = int((tMar - tJan).days)
    deadlineApr = int((tApr - tJan).days)
    try:
        fout = open(outdir+'group-commit-trend.csv','wb')
        cw = csv.writer(fout)
        cw.writerow(['group_id', 'sum of commits over time'])
        for gp in groups:
            print gp
            fig = plt.figure()
            data = group_commits[gp][1]
            plt.plot(data, linewidth=2, color='orange')
            plt.axvline(deadlineFeb, linestyle='--')
            plt.axvline(deadlineMar, linestyle='--')
            plt.axvline(deadlineApr, linestyle='--')
            plt.axis([0, totalDays, 0, max(data)*1.1])
            fig.savefig(outdir + gp + '-commit_trend.png')
            term = data
            term.insert(0, gp)
            cw.writerow(term)
        fout.close()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()