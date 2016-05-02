#!/usr/bin/env python
import csv
import numpy as np

indir = './badSmellScoreCSV/'
outdir = './result/'

def lack_of_communication(allBadSmells):
    col = [2, 3, 4, 5, 10]
    weights = np.array([1, 1, 1, 1, 1])
    scores = dict()
    for gp in allBadSmells.keys():
        features = np.array([allBadSmells[gp][i-1] for i in col])
        scores[gp] = features.dot(weights)
    return scores

def delayed_delivery(allBadSmells):
    # col 14, 9
    col = [9, 14]
    weights = np.array([1, 1])
    scores = dict()
    for gp in allBadSmells.keys():
        features = np.array([allBadSmells[gp][i-1] for i in col])
        scores[gp] = features.dot(weights)
    return scores


def unbalanced_contribution(allBadSmells):
    # col 2,3,4,5, 10, 11
    col = [2, 3, 4, 5, 10, 11]
    weights = np.array([1, 1, 1, 1, 1, 10])
    scores = dict()
    for gp in allBadSmells.keys():
        features = np.array([allBadSmells[gp][i-1] for i in col])
        scores[gp] = features.dot(weights)
    return scores


def poor_planning(allBadSmells):
    # col 1, 6, 7, 8, 12, 13, 15, 16
    col = [1, 6, 7, 8, 12, 13, 15, 16]
    weights = np.array([1, 1, 1, 1, 1, 1, 1, 1])
    scores = dict()
    for gp in allBadSmells.keys():
        features = np.array([allBadSmells[gp][i-1] for i in col])
        scores[gp] = features.dot(weights)
    return scores

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
                #print allBadSmells[row[0]]
            rNum += 1
    score1 = lack_of_communication(allBadSmells)
    score2 = delayed_delivery(allBadSmells)
    score3 = unbalanced_contribution(allBadSmells)
    score4 = poor_planning(allBadSmells)
    

if __name__ == "__main__":
    main()