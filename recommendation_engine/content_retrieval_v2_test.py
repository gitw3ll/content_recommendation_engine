from content_retrieval_v2 import ContentRetrieval

path =  r'C:\Users\Vikram\OneDrive\Documents\Videos\Documents\RecommenderModelData'

c = ContentRetrieval()

c.load_preprocess(path)

a = c.retrieve_content(user_id=50, wellness_metric='Emotional Score', similar_users=5, content_per_user=3)

print(a)