
from django.urls import path
from . import views

urlpatterns = [
    path('adm/allbooks', views.all_books, name='admin_allbooks'),
    path('adm/addbook', views.add_book, name='admin_addbooks'),
    
    ]
