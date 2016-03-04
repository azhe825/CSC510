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

### Three Different Attempts

For 4 and 5 shown above, three different attempts have been tried.

 - **a) Brutal**: ignore all the credits, just put everything we get into training set when the threshold is reached. **Benefit**: simple.
 - **b) Credit**: Shown in Design. Put emails with top N credit of each folder into the training set. **Benefit**: more balance over folders, wrongly predicted emails have more chance to get into the training set.
 - **c) Wrong**: During each iteration, only put the wrongly predicted emails into the training set. **Benefit**: wrongly predicted emails are guaranteed to be put into training set, correctly predicted emails will be totally ignored.

### Code

[See](https://github.com/azhe825/CSC510/blob/master/testEmails/test.py)

### Result for March 1st

**Brutal**

![file](https://github.com/azhe825/CSC510/blob/master/Results/semi_brutal.png)

**Credit**

![file](https://github.com/azhe825/CSC510/blob/master/Results/semi_credit.png)

**Wrong**

![file](https://github.com/azhe825/CSC510/blob/master/Results/semi_wrong.png)

**Comparison**

![file](https://github.com/azhe825/CSC510/blob/master/Results/semi_methods.png)

### Conclusion

Performance does improve after adding new training examples. 

b) **Credit** is performing the best.

Need to incorporate this solution into the product.
