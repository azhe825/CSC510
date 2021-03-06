# CSC_510_group_c
Academic Project - CSC 510 - Software Engineering

## Group Members:
 - Zhe Yu (unit ID: zyu9, github ID: azhe825)
 - Amritanshu Agrawal (unit ID: aagrawa8, github ID: amritbhanu)
 - Di Chen (unit ID: dchen20, github ID: dichen001)
 - Shijie Li (unit ID: sli41, github ID: imaginationsuper)

## Quick Links:
1. [Repo's issue page] (https://github.com/azhe825/CSC510/issues) <br />

2. [Repo's milestone page] (https://github.com/azhe825/CSC510/milestones) <br />

3. [Repo's contributor page](https://github.com/azhe825/CSC510/graphs/contributors) <br />


## Demos

NO demos yet, have not developed the GUI. Our plan is to both code and test solution in Feb and build GUI with the best combination of solutions in Mar.


### Overall Design

1. user define the folders. (folder names, put at least 10 emails in each folder)

2. train classifier

3. new email comes in, classifier predict a folder and put the email into that folder.

4. user manipulates emails (reply, forward, delete, star, move into another folder...)

5. 3 and 4 can happens not in a specific sequence.

**Information** of new comming emails can be retrieved from 4:
 - if user move it into another folder, it is definitely wrongly predicted at first and now we get the true answer. This kind of email is most valuable.
 - if user reply, forward it, it is probably true that the email is correctly predicted. This kind of email has some value.

### Assumptions

User is OK with having at least 10 training examples in each folder.

All the folders user defined are content-related.

## Problem and Solutions

a. **Problem:** Training set is small. Has only 10 examples in each class.

b. **Solutions:**
 - **Supervised Learning**: Try different classification methods to find the best classifier on small training set.
 - **Semi-supervised Learning**: Add examples into training set according to user activities. Retrain classifier.
 - **Unsupervised Learning**: Clustering before training to provide extra knowledge (topics). 

## Reports
a. [Data management + Preprocessing by Shijie Li](https://github.com/azhe825/CSC510/blob/master/report/Mar/Data.Collection.and.Pre-processing.md) <br />

b. Three solutions to improve performance: <br />
[Solution1 by Di Chen] (https://github.com/azhe825/CSC510/blob/master/report/Mar/supervised_learning.md) <br />
[Solution2 by Zhe Yu] (https://github.com/azhe825/CSC510/blob/master/report/Mar/semi-supervised.md) <br />
[Solution3 Amritanshu Agrawal] (https://github.com/azhe825/CSC510/blob/master/report/Mar/Unsupervised_Learning.md) <br />

## Plan for March:

[milestone1 - "Build a simple GUI"] (https://github.com/azhe825/CSC510/milestones/GUI%20Build) <br/>
[milestone2 - "Combine all three solutions to have the best"] (https://github.com/azhe825/CSC510/milestones/Combine%20all%20three%20solutions%20to%20have%20the%20best)<br/>
[milestone3 - "Implement best solution with GUI"] (https://github.com/azhe825/CSC510/milestones/Implement%20best%20solution%20with%20GUI)<br/>
[milestone4 - "Testing"] (https://github.com/azhe825/CSC510/milestones/Testing%20for%20solutions)<br/>
