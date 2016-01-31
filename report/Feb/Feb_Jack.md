
There are two main problems with the email categorizaiton in existing email applications. 

Fisrt of all, even though automatic categorization services are usually offered in the Email applications like Gmail and Yahoo Mail, they only categorize emails into several default folders, such as Promotions, Updates, Social, Forums and so on. For common email users, the default forders have covered most of their daily emails, but it is far away from ‘enough' for heavy email users who have to categorize their emails in a more detailed way. 

Another problem we notice is that the existing automatic categorization systems only ask for users' feedback in a q uite passive way. For example, the feedback buttons are usrally hidden in the second level of their user interface, and they seldom ask for feedback from users to see if their categorization is correct or not.

So our goal is to offer users an active and automatic email categorization, which is a combination of new user interaction and underlying classification algorithm.

The solution is fist to design a new categorization logic. Like other email applications, we will classify emails into serveral default folders, which is based on massive email training set. Then, we will actively ask the user for feadback in a non-disturbing way. User can choose the right folder to put the new-coming email or create new folder if they like. Finally, based on our users' categorization record, we will extract user-specific features for each user to train our classifier.

Figure 1. below show the interface when a new email arrives. It will pop up a message in the purple frame, asking the user if the email is put into the right folder by our system. It will fade out automatically within 5 seconds if user leave it alone, which means user tacitly acknowledge the categorization is correct. If users find it is put into a wrong folder, then they can click the green button, which will pop up several other folders for users to choose from. Besides, users can click “Create New Folder” if none of the other existing folders meet their need. Once a new folder is created and the email is put into the new folder, our system will add this to our training set, so that similar emails will be categorized into this new folder automatically in the future.


![Demo](https://cloud.githubusercontent.com/assets/15117843/12694127/4ce0bcf4-c6f0-11e5-8e13-49d214c9c59a.png "Demo")

