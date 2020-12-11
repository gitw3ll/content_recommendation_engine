# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 07:27:08 2020

@author: Vikram
"""

import pandas as pd
import os
import numpy as np
import scipy.sparse as sparse
import implicit
from implicit.nearest_neighbours import bm25_weight
from flask import Flask, request, render_template, jsonify

articles = pd.read_csv(r'C:\Users\Vikram\OneDrive\Documents\Videos\Documents\shared_articles.csv\shared_articles.csv')

interactions = pd.read_csv(r'C:\Users\Vikram\OneDrive\Documents\Videos\Documents\users_interactions.csv\users_interactions.csv')

articles = articles.drop(columns=['authorUserAgent', 'authorRegion', 'authorCountry'])

interactions = interactions.drop(columns=['userAgent', 'userRegion', 'userCountry'])

articles = articles[articles['eventType'] == 'CONTENT SHARED']

df = pd.merge(interactions[['contentId', 'personId', 'eventType']], articles[['contentId', 'title']], how='inner', on='contentId')

df['eventType'].value_counts()

event_type_strength = {
   'VIEW': 1.0,
   'LIKE': 2.0, 
   'BOOKMARK': 3.0, 
   'COMMENT CREATED': 4.0,
   'FOLLOW': 5.0,  
}

df['eventStrength'] = df['eventType'].apply(lambda x: event_type_strength[x])

df = df.drop_duplicates()
df = df.groupby(['personId', 'contentId', 'title']).sum().reset_index()

df['eventStrength'].value_counts()

df['title'] = df['title'].astype("category")

df['personId'] = df['personId'].astype("category")

df['contentId'] = df['contentId'].astype("category")

df['person_id'] = df['personId'].cat.codes

df['content_id'] = df['contentId'].cat.codes

sparse_content_person = sparse.coo_matrix((df['eventStrength'].astype(float), (df['content_id'], df['person_id'])))

#sparse_person_content = sparse.csr_matrix((df['eventStrength'].astype(float), (df['person_id'], df['content_id'])))

sparse_content_person = bm25_weight(sparse_content_person, K1=100, B=0.8)

data = sparse_content_person.tocsr()

model = implicit.als.AlternatingLeastSquares(factors=64, regularization=0.001, use_native=True, use_cg=True)

model.fit(data)

user_data = data.T.tocsr()

recommendations = model.recommend(50, user_data, N=10)

#print(recommendations)

item_indices, scores = map(list, zip(*recommendations))

#print(item_indices)

titles = []

for index in item_indices:
    titles.append(df['title'][index])

#print(titles)

results = pd.DataFrame({'title': titles, 'score': scores})

print(results)


df.loc[df['person_id'] == 50].sort_values(by=['eventStrength'], ascending=False)[['title', 'eventStrength']].head(10)








