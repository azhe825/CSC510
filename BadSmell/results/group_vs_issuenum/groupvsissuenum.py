import csv
import os

indir = '../../dataCollectionInCSV_last/'
outdir = './'
groupvsissuenumber = dict()

def count_issue(filename):
    counter = 0
    group = filename.split('-issue')[0]
    print group
    with open(indir+filename, 'rb') as fin:
        cr = csv.reader(fin)
        for _ in cr:
            counter += 1
    groupvsissuenumber.update({group: counter-1})



def main():
    for fn in os.listdir(indir):
        if (not os.path.isdir(fn)) and ('.csv' in fn) and ('-issue' in fn):
            count_issue(fn)
    with open('group_vs_issuenum.csv', 'wb') as fout:
        cw = csv.writer(fout)
        cw.writerow(["group_id", "number of issues"])
        cw.writerows(groupvsissuenumber.items())


if __name__ == "__main__":
    main()