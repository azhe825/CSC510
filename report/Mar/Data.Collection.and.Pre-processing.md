## Data Collection And Preprocessing

### Enron Email Dataset:
We use the enron email dataset as our experiment data. It contains a large quantity of email files in standard MIME format. We pick up the first seven user folders with the most email files in this stage.

### Data Preprocessing:

-  For each user, pick the categorized folders with more than 10 emails (for enough training size) and less than 100 emails (for computational limits). We also remove the common folders, such as 'all_document', '_sent' etc. Then we save the selected emails under the same user name as a personalized data set.

-  For each email chosen in step 1, we first use Python email package to remove the header of email and extract extract the email subject and body. Then we filter subject and body by removing all non-character tokens and save it into list of words with the folder name(or path) as its category label.

-  For each filtered email, we apply convertion methods to mapping words into real-number vectors. Then these vectors can be served as input to popular classifiers.

### Results:
The collected and filtered data are stored in the following link:
(https://raw.githubusercontent.com/azhe825/CSC510/master/testEmails/dataset1.txt)

Transformed data are integrated in the solution codes.
