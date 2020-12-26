import os
import numpy as np
import pandas as pd
from collections import deque


class ContentRetrieval:
    def __init__(self):
        self.event_type_strength = {
            'VIEW': 1.0,
            'LIKE': 2.0, 
            'BOOKMARK': 3.0, 
            'COMMENT CREATED': 4.0,
            'FOLLOW': 5.0,  
            }
        self.articles_df = None
        self.interactions_df = None
        self.score_data = None
        self.content_data = None
        
    def load_preprocess(self, data_directory):
        """
        """
        #Preprocess and load user content data
        
        self.articles_df = pd.read_csv(os.path.join(data_directory, 'shared_articles.csv'))
        self.interactions_df = pd.read_csv(os.path.join(data_directory, 'users_interactions.csv'))

        self.articles_df = self.articles_df.drop(columns=['authorUserAgent', 'authorRegion', 'authorCountry'])
        self.interactions_df = self.interactions_df.drop(columns=['userAgent', 'userRegion', 'userCountry'])
        self.articles_df = self.articles_df[self.articles_df.eventType == 'CONTENT SHARED']

        df = pd.merge(self.interactions_df[['contentId', 'personId', 'eventType']], self.articles_df[['contentId', 'title']], how='inner', on='contentId')
        df['eventStrength'] = df['eventType'].apply(lambda x: self.event_type_strength[x])
        
        df = df.drop_duplicates()
        df = df.groupby(['personId', 'contentId', 'title']).sum().reset_index()

        df['title'] = df['title'].astype("category")
        df['personId'] = df['personId'].astype("category")
        df['contentId'] = df['contentId'].astype("category")
        df['person_id'] = df['personId'].cat.codes
        df['content_id'] = df['contentId'].cat.codes
        
        self.content_data = df
        
        #Load user wellness score data
        
        self.scores_data = pd.read_csv(os.path.join(data_directory, 'user_wellness_scores.csv'))
        


    def retrieve_content(self, user_id, wellness_metric, similar_users=3, content_per_user=5):
        """
        """
        
        user_content = list(self.content_data.loc[self.content_data['person_id'] == user_id]['title'])
        user_content = deque([user_content])
        
        user_score = self.scores_data.at[user_id, wellness_metric]
        
        closest_emotional = self.scores_data.iloc[(self.scores_data[wellness_metric] - user_score).abs().argsort()[:similar_users]]
        closest_ids_list = list(closest_emotional['personId'])
        
        similar_content = deque([])

        for num in closest_ids_list:
            similar_content.append(list(self.content_data.loc[self.content_data['person_id'] == num]['title'][:content_per_user]))
            
            for content in user_content:
                if content in similar_content: 
                    similar_content.remove(content)

        similar_content = np.concatenate(similar_content, axis=0).tolist()
        
        return similar_content