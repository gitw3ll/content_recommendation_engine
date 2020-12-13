import os
import numpy as np
import pandas as pd
import scipy.sparse as sparse
import implicit
from implicit.nearest_neighbours import bm25_weight

class RecommenderModel:
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
        self.model = None
        self.sparse_matrix = None
        self.data = None
        
    def load_preprocess(self, data_directory):
        """
        """
        
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
        
        self.data = df


    def setup_model(self, k1=1.2, b=0.75, factors=64, regularization=0.001, use_native=True, use_cg=True):
        """
        """
        
        # Converting to coordinate format to increase space efficiency
        sparse_content_person = sparse.coo_matrix((self.data['eventStrength'].astype(float), (self.data['content_id'], self.data['person_id'])))
        #print(f'Before bm25: {sparse_content_person}')
        sparse_content_person = bm25_weight(sparse_content_person, K1=k1, B=b)
        #print(f'After bm25: {sparse_content_person}')
        
        self.sparse_matrix = sparse_content_person.tocsr()
        
        self.model = implicit.als.AlternatingLeastSquares(
            factors=factors, 
            regularization=regularization, 
            use_native=use_native, 
            use_cg=use_cg
            )

    def train(self):
        """
        """
        # Train model

        self.setup_model()
        self.model.fit(self.sparse_matrix)
    
    def predict(self, user_index, n_predict=10):
        """
        """
        
        user_data = self.sparse_matrix.T.tocsr()
        recommendations = self.model.recommend(user_index, user_data, N=n_predict)

        item_indices, scores = map(list, zip(*recommendations))
        titles = [self.data['title'][index] for index in item_indices]

        return dict(zip(titles, scores))
