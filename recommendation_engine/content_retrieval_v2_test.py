from content_retrieval_v2 import ContentRetrieval

path =  r'C:\path\to\RecommenderModelData'

cont_ret = ContentRetrieval()

cont_ret.load_preprocess(path)

similar_content = cont_ret.retrieve_content(user_id=50, wellness_metric='Emotional Score', similar_users=5, content_per_user=3)

print(similar_content)
