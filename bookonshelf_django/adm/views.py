#from csv import writer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
#from .forms import LoginForm
from books.forms import WritersForm, BooksForm
from books.models import Writers, Books
from main import views as main_views
from main.decorators import has_admin_permission, has_user_permission

@has_admin_permission
def all_books(request):
    books = Books.objects.all()
    return render(request, "adm/allbooks.html", {'books': books})

#def add_book(request):
#    writersform = WritersForm()
#    data = {
#        'writersform': writersform
#        }
#    return render(request, 'adm/addbook.html', data)
@has_admin_permission
def add_book(request):
    error = ''
    if request.method == 'POST':
        booksform = BooksForm(request.POST)
        if booksform.is_valid():
            booksform.save()
            return redirect('admin_allbooks') 
        else: 
            error = 'Форма заполнена неверно'
    booksform = BooksForm()
    
    data = {
        
        'booksform': booksform,
        'error': error
        
        } 
    return render(request, "adm/addbook.html", data)

@has_admin_permission
def add_writer(request):
    error = ''
    if request.method == 'POST':
        writersform = WritersForm(request.POST)
        if writersform.is_valid():
            writersform.save()
            return redirect('admin_allbooks')
        else:
            error = 'Форма заполнена неверно'
    writersform = WritersForm()

    data = {

        'writersform': writersform,
        'error': error

    }
    return render(request, "adm/addwriter.html", data)