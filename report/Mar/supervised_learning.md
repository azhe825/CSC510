# Supervised Learning
## Methedology
- Select 7 users from Enron Email dataset who has the most sub-folders
- Remove the sub-folders which has less than 10 emails.
- Use *term frequency* as the feature metric
- for each folder under each user, we only randomly select 10 eamils as the training dataset.
- Using three different classifiers, i.e. Linear SVM, KNN and DT.

Also tried using Word Vector to transform each email as a vector. So we map our emails into vectors in the sentiment-related space. Then using different classifiers to test its performance. 


## Code
see [here](https://github.com/azhe825/CSC510/tree/master/testEmails)
## Results
#### Figure 1:  Perfomance on different users.
![sum](https://raw.githubusercontent.com/azhe825/CSC510/master/Results/comp_classifier.png)

#### Figure 2: Incremental Learning Results
![Summery](https://raw.githubusercontent.com/azhe825/CSC510/master/Results/semi_classifier.png)

## Conclusion
- Word Vector performs poorly on this task. Right now, it only achives:
  - Precision:  0.0028935031532752618
  - Recall:     0.013399361812185769
  - F-score:    0.0036415252615324602
  Will give up in the future. 
- As you can see in Figure 1, the prediction performance varies among different users. It is because some users may label them emails more generally, while the others more precisely. Also, the content of the email sub-folders also matters.
- Also, we can see SVM performs better than DT and KNN.

- For Figure 2, we can know that, averagely, the more training data we have, the better our prediction will be. But, generally speaking, the improvements is not as big as we have expected.


