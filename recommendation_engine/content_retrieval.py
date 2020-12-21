import numpy as np
import pandas as pd

#Generate an array of 1000 user IDs

user_ids = np.arange(start=1, stop=1001, step=1)

#np.random.random(n) generates n random values between 0 and 1
#To get n values between a and b excluding b, compute (b - a)*np.random.random(n) + a
#Here we generate 3 sets of 1000 values with our upper bounds as 30 and lower bounds as 1
#The 3 sets represent different mental prosociality scores, emotional scores, and physical diet scores

mental_scores = 29*np.random.random(1000) + 1 
emotional_scores = 29*np.random.random(1000) + 1
diet_scores = 29*np.random.random(1000) + 1

#Generate an array containing WQ scores by summing the above three arrays

wq = mental_scores + emotional_scores + diet_scores

#Store all the data in a dictionary
values = {'personId': user_ids, 'Mental Score': mental_scores, 'Emotional Score': emotional_scores, 'Diet Score': diet_scores, 'WQ': wq}

#Use the dictionary to create a dataframe
data = pd.DataFrame(data=values)

#Add basic content retrieval functionality
#We assume that there's a separate dataset that contains every interaction for each user
#Say that a particular user (we assume their ID = 50) is feeling in whatever way
#We ask them to input a number representing their current Emotional Score. Here we assume the number is 5.

user_emotional_score = 5

#Get dataframe of the three users with closest Emotional Score to 5
closest_emotional = data.iloc[(data['Emotional Score'] - user_emotional_score).abs().argsort()[:3]]
print(closest_emotional)

closest_ids_list = closest_emotional['personId'].values

#In user interaction dataset assume the same weighting scheme for the implicit recommendation algorithm applies:
'''event_type_strength = {
            'VIEW': 1.0,
            'LIKE': 2.0, 
            'BOOKMARK': 3.0, 
            'COMMENT CREATED': 4.0,
            'FOLLOW': 5.0,  
            }
'''

#Dataset is called df_interactions and has columns 'title', 'personId', 'contentId', 'eventStrength'

#Get top 5 contents for 3 closest users and display them

'''
content_list = []

df_interactions = df_interactions.groupby(['personId', 'contentId', 'title']).sum().reset_index()

for user_id in closest_ids_list:
    content_list.append(df_interactions.loc[df_interactions['personId'] == user_id]['title'][:5])
    
content_list = np.concatenate(content_list, axis=0).tolist()

print(content_list)
'''