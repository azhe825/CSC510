__author__ = 'amrit'

import os
import re
import csv

filepath = 'dump/'
filepath1 = 'results/'
with open(filepath1 + 'features.csv', 'w') as csvfile:
    fieldnames = ['groupid', 'user','activities']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for root, dirs, files in os.walk(filepath, topdown=False):
        for name in files:
            a = os.path.join(root, name)
            dict = {}

            with open(a, 'r') as f:
                for l in f.readlines():
                    t = l.split('|')
                    for x in t:
                        match = re.match(r'.*\swhen :\s(.*),\suser :\s(.*),.*', x, re.M | re.I)
                        if match:
                            if match.group(2) != 'user19' and match.group(2) != 'user5' and match.group(2) != 'history':
                                if match.group(2) in dict.keys():
                                    dict[match.group(2)] += 1
                                else:
                                    dict[match.group(2)] = 1
                        else:
                            match = re.match(r'.*\swhen :\s(.*),\suser :\s(.*)\s', x, re.M | re.I)
                            if match:
                                if match.group(2) != 'user19' and match.group(2) != 'user5' and match.group(2) != 'history':
                                    if match.group(2) in dict.keys():
                                        dict[match.group(2)] += 1
                                    else:
                                        dict[match.group(2)] = 1
                if 'amritanshu' in dict.keys():
                    dict['user34'] += dict['amritanshu']
                    dict.pop('amritanshu')
            for i in dict.keys():
                writer.writerow({'groupid': name.split(".txt")[0], 'user': i, 'activities':dict[i]})