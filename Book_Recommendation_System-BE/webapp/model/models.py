from django.db import models
import pickle

pickle_file_path = 'C:/Users/User/Desktop/Book Recommendation System/webapp/mlModel/model_knn.pkl'

with open(pickle_file_path, 'rb') as file:
    knn_model = pickle.load(file)

