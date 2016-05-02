#!/usr/bin/env python
import csv
import numpy as np

indir = './badSmellScoreCSV/'
outdir = './result/'

def lack_of_communication(allBadSmells):
    # col 2, 3, 4, 5, 10
    weights = np.array([1, 1, 1, 1, 1])
    scores = dict()
    for gp in allBadSmells.keys():
        features = np.array(allBadSmells[gp])
        scores[gp] = features
    return 0

def delayed_delivery(allBadSmells):
    # col 14, 9
    return 0


def unbalanced_contribution(allBadSmells):
    # col 2,3,4,5, 10, 11
    return 0

def poor_planning(allBadSmells):
    # col 1, 6, 7, 8, 9, 11, 12, 13, 14
    return 0

def main():
    allBadSmells = dict()
    with open(indir+'allBadSmell.csv') as fin:
        cr = csv.reader(fin)
        rNum = 0
        for row in cr:
            if rNum == 0:
                header = row
            else:
                allBadSmells[int(row[0])] = map(float, row[1:])
                print allBadSmells[row[0]]
            rNum += 1
    score1 = lack_of_communication(allBadSmells)
    score2 = delayed_delivery(allBadSmells)
    score3 = unbalanced_contribution(allBadSmells)
    score4 = poor_planning(allBadSmells)


    

if __name__ == "__main__":
    main()