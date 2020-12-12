from recommender_model import RecommenderModel

DATA_DIRECTORY = 'data/'

rec = RecommenderModel()
rec.load_train_data(DATA_DIRECTORY)
rec.train()
pred = rec.predict(user_index=50)
print(f'predictions: {pred}')