## Unsupervised Learning
### Feature extraction and Learner
- The tf score is used as data to do LDA analysis (unsupervised learning).
- According to different amount of top topics, the top words occuring in that is used as a new word corpus.
- The new tf_scores generated (by lda) for this word corpus is used to train an SVM classifier.
- For one random target label, F Score is measured.

### Code
- [Here] (https://github.com/azhe825/CSC510/blob/master/testEmails/lda.py)

### Results

- Results with top 100 topics
![file](https://github.com/azhe825/CSC510/blob/master/Results/lda/lda_SVM_100.png?raw=true)

- Results with top 50 topics
![file](https://github.com/azhe825/CSC510/blob/master/Results/lda/lda_SVM_50.png?raw=true)

- Results with top 20 topics
![file](https://github.com/azhe825/CSC510/blob/master/Results/lda/lda_SVM_20.png?raw=true)

### Conclusion

- Some of the F_scores are reaching 0.7-0.8. The features extracted by LDA for that particular label is self sufficient to keep a good F_score
- Some of the median scores are 0. As randomly one target is chosen and that target label didn't occur in the testing set.
 
### Future

- Use the LDA feature scores rather than tf scores to feed into the classifier.
