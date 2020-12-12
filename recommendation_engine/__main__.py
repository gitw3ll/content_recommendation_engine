from recommender_model import RecommenderModel

DATA_DIRECTORY = 'recommendation_engine/data/'

rec = RecommenderModel()
rec.load_train_data(DATA_DIRECTORY)
rec.train()
pred = rec.predict(user_index=50)
print(pred)