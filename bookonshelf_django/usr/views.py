from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
#from .forms import LoginForm
from books.forms import WritersForm, BooksForm, GenresForm, LanguagesForm, BookSearchForm
from books.models import Writers, Books, Genres, Languages
from django.db.models import Q
from main import views as main_views
from main.decorators import has_admin_permission, has_user_permission

@has_user_permission
def all_books(request):
    books = Books.objects.all()
    booksearchform = BookSearchForm()
    data = {
        'books': books,
        'booksearchform': booksearchform
    }
    return render(request, "usr/allbooks.html", data)