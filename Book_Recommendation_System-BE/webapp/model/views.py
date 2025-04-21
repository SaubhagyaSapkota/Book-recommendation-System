from django.shortcuts import render
from django.http import JsonResponse
from .models import knn_model
import numpy as np
import pandas as pd
import pickle


# Use the full path to the pickle file
pickle_file_path_1 = 'C:/Users/User/Desktop/Book Recommendation System/webapp/mlModel/final_ratings.pkl'
pickle_file_path_2 = 'C:/Users/User/Desktop/Book Recommendation System/webapp/mlModel/book_name.pkl'
pickle_file_path_3 = 'C:/Users/User/Desktop/Book Recommendation System/webapp/mlModel/book_pivot.pkl'
pickle_file_path_4 = 'C:/Users/User/Desktop/Book Recommendation System/webapp/mlModel/final_ratings_for_top_recommend.pkl'

# Load the pickle files
with open(pickle_file_path_1, 'rb') as file:
    final_ratings = pickle.load(file)

with open(pickle_file_path_2, 'rb') as file:
    book_names = pickle.load(file)

with open(pickle_file_path_3, 'rb') as file:
    book_pivot = pickle.load(file)

with open(pickle_file_path_4, 'rb') as file:
    book_details = pickle.load(file)

books = list(book_names)

def get_recommend(book):
    book_id = np.where(book_pivot.index == book)[0][0]
    recommended_books = []
    distance, suggestion = knn_model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=7)
    recommended_books = list(book_pivot.iloc[suggestion[0]].index)
    return recommended_books

def get_image_url(book):
    book_image_url = None
    try:
        book_image_url = final_ratings.loc[final_ratings['Book-Title'] == book, 'Image-URL-S'].iloc[0]
    except IndexError:
        pass
    return book_image_url

def get_genre_detail(genre_list, book_lists):
    genre_counts = book_lists['Book-Genre'].value_counts().to_dict()
    genre_data = []
    for genre in genre_list:
        genre_count = genre_counts.get(genre, 0)*4
        genre_data.append({'genre': genre.capitalize(), 'genre_count': genre_count})
    genre_data.sort(key=lambda x: x['genre_count'], reverse=True)
    return genre_data

def get_recommendations_with_images(recommendations):
    recommendations_with_images = []
    for recommendation in recommendations:
        image_url = get_image_url(recommendation)
        author = final_ratings.loc[final_ratings['Book-Title'] == recommendation, 'Book-Author'].iloc[0]
        publication_year = final_ratings.loc[final_ratings['Book-Title'] == recommendation, 'Year-Of-Publication'].iloc[0]
        recommendations_with_images.append({'book_name': recommendation, 'image_url': image_url, 'author': author, 'publication_year': publication_year})
    return recommendations_with_images

def get_top_book_details(top_book_name):
    book_with_data = []
    for books in top_book_name:
        isbn = book_details.loc[book_details['Book-Title'] == books, 'ISBN'].iloc[0]
        rating = round(book_details.loc[book_details['Book-Title'] == books, 'Avg-Rating'].iloc[0], 2)
        book_with_data.append({'book_name': books, 'isbn': isbn, 'avg_ratings': rating})
    return book_with_data

def index(request):
    return render(request, 'index.html', {'books': books})

def second(request):
    book_name = request.GET.get('book')  # Get the selected book name from the request
    recommendations = []
    book_image_url = None
    publisher = None
    genre = None
    ratings = None
    author = None
    publication_date = None
    recommended_image_url = []
    if book_name:
        recommendations = get_recommend(book_name)
        recommended_data = get_recommendations_with_images(recommendations)
        try:
            book_image_url = final_ratings.loc[final_ratings['Book-Title'] == book_name, 'Image-URL-S'].iloc[0]
            publisher = final_ratings.loc[final_ratings['Book-Title'] == book_name, 'Publisher'].iloc[0]
            genre = book_details.loc[book_details['Book-Title'] == book_name, 'Book-Genre'].iloc[0].capitalize()
            ratings = round(book_details.loc[book_details['Book-Title'] == book_name, 'Avg-Rating'].iloc[0],2)
            author = final_ratings.loc[final_ratings['Book-Title'] == book_name, 'Book-Author'].iloc[0]
            publication_date = final_ratings.loc[final_ratings['Book-Title'] == book_name, 'Year-Of-Publication'].iloc[0]
        except IndexError:
            pass
    return render(request, 'secondpage.html', {'book_name': book_name, 'publisher': publisher, 'genre': genre, 'ratings':ratings, 'author': author, 'publication_date': publication_date, 'recommended_data': recommended_data, 'book_image_url': book_image_url})

def genres(request):
    unique_books = book_details.drop_duplicates(subset=['Book-Title'], keep='first')
    unique_genres = unique_books['Book-Genre'].unique()
    genre_detail = get_genre_detail(unique_genres, unique_books)
    return render(request, 'genres.html', {'genre_detail': genre_detail, 'books': books})

def top_authors(request):
    author_counts = book_details.groupby('Book-Author').size()
    top_authors = author_counts.sort_values(ascending=False).index.tolist()
    top_authors = top_authors[:10]
    return render(request, 'top_authors.html', {'top_authors': top_authors})

def top_book(request):
    unique_books = book_details.drop_duplicates(subset=['Book-Title'])
    top_10_books = unique_books.sort_values(by='Avg-Rating', ascending=False)['Book-Title']
    top_10_books = top_10_books[:10]
    top_books = list(top_10_books)
    top_book_data = get_top_book_details(top_books)
    return render(request, 'top_book.html', {'top_book_data': top_book_data, 'books': books})

def top_publisher(request):
    publisher_counts = book_details.groupby('Publisher').size()
    top_publisher = publisher_counts.sort_values(ascending=False).index.tolist()
    top_publisher = top_publisher[:10]
    return render(request, 'top_publisher.html', {'top_publisher': top_publisher, 'books': books})

