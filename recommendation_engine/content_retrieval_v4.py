import numpy as np
import sqlite3
import dask.dataframe as dd
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
        
    def load_preprocess(self, database_directory):
        """
        """
        
        conn = sqlite3.connect(database_directory)
        
        self.articles_df = dd.read_sql_table('content_data', conn)
        self.interactions_df = dd.read_sql_table('user_data', conn)

        df = self.articles_df.merge(self.interactions_df, on='content_id')
        df['eventStrength'] = df['event_type'].apply(lambda x: self.event_type_strength[x])
        
        df = df.drop_duplicates()
        df = df.groupby(['person_id', 'content_id', 'title']).sum().reset_index()

        df['title'] = df['title'].astype('category')
        df['person_id'] = df['person_id'].astype('category')
        df['content_id'] = df['content_id'].astype('category')
        df['personId'] = df['person_id'].cat.codes
        df['contentId'] = df['content_id'].cat.codes
        
        self.content_data = df
        
        #Load user wellness score data
        
        self.scores_data = dd.read_sql_table('scores_data', conn)
        


    def retrieve_content(self, user_id, wellness_metric, similar_users=3, content_per_user=5):
        """
        """
        
        user_content = list(self.content_data.loc[self.content_data['personId'] == user_id]['title'])
        user_content = deque([user_content])
        
        user_score = self.scores_data.at[user_id, wellness_metric]
        
        closest_emotional = self.scores_data.iloc[(self.scores_data[wellness_metric] - user_score).abs().argsort()[:similar_users]]
        closest_ids_list = list(closest_emotional['personId'])
        
        similar_content = deque([])

        for num in closest_ids_list:
            similar_content.append(list(self.content_data.loc[self.content_data['personId'] == num]['title'][:content_per_user]))
            
            for content in user_content:
                if content in similar_content: 
                    similar_content.remove(content)

        similar_content = np.concatenate(similar_content, axis=0).tolist()
        
        return similar_content