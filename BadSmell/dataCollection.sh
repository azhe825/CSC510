#!/bin/bash
count=1
for repo in `cat repos.txt`
do python gitable-sql.py $repo $(echo group${count})
count=$((count+1))
done
