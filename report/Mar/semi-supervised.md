## Feature: Incremental Learning

### Design

1. user define the folders. (folder names, put at least 10 emails in each folder)

2. train classifier

3. new email comes in, classifier predict a folder and put the email into that folder. All new comming emails are asigned a credit 0.

4. what can happen to these new emails:
 - a) remains untouched, credit 0
 - b) user reply, read, forward the email without moving it into another folder. Assign a credit of 0.5. (correctly predicted emails)
 - c) user move the email into another folder. Assign a credit of 1.0. (wrongly predicted emails)

5. once the total credit of the unused email has exceed a certain threshold (e.g. 100), emails with top N (e.g. 10) credit in each folder are put into the training set.

6. go to 2.

### Result for March 1st

![file](https://github.com/azhe825/CSC510/blob/master/Results/semi_SVM_.png)

### Conclusion

Performance does improve after adding new training examples. Need to incorporate this solution into the product.
