
from django.urls import path
from . import views

urlpatterns = [
    path('usr/allbooks', views.all_books, name='user_allbooks'),
    path('usr/booksearch', views.book_search, name='user_booksearch'),
    path('usr/books/<int:book_id>/', views.book_details, name='user_bookdetails'),
    path('usr/borrowbook/<int:book_id>/', views.book_borrow, name='user_borrowbook'),
    path('usr/mybooks', views.mybooks, name='user_mybooks'),
]
