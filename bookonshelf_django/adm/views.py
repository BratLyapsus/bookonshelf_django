from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
#from .forms import LoginForm
from books.forms import WritersForm, BooksForm, GenresForm, LanguagesForm, BookSearchForm
from books.models import Writers, Books, Genres, Languages
from main import views as main_views
from main.decorators import has_admin_permission, has_user_permission

@has_admin_permission
def all_books(request):
    books = Books.objects.all()
    booksearchform = BookSearchForm()
    data = {
        'books': books,
        'booksearchform': booksearchform
    }
    return render(request, "adm/allbooks.html", data)

@has_admin_permission
def add_book(request):
    error = ''
    if request.method == 'POST':
        booksform = BooksForm(request.POST, request.FILES)
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

def add_genre(request):
    error = ''
    if request.method == 'POST':
        genresform = GenresForm(request.POST)
        if genresform.is_valid():
            genresform.save()
            return redirect('admin_allbooks')
        else:
            error = 'Форма заполнена неверно'
    genresform = GenresForm()

    data = {

        'genresform': genresform,
        'error': error

    }
    return render(request, "adm/addgenre.html", data)
def add_language(request):
    error = ''
    if request.method == 'POST':
        languagesform = LanguagesForm(request.POST)
        if languagesform.is_valid():
            languagesform.save()
            return redirect('admin_allbooks')
        else:
            error = 'Форма заполнена неверно'
    languagesform = LanguagesForm()

    data = {

        'languagesform': languagesform,
        'error': error

    }
    return render(request, "adm/addlanguage.html", data)

#def book_search(request):

#    booksearchform = BookSearchForm()
#    data = {
#        'booksearchform': booksearchform
#    }
#    return render(request, "adm/booksearch.html", data)
def search_result(request):
    return render(request, "adm/searchresult.html")
def book_search(request):
    data = {}  # Initialize empty data dictionary
    error = ''

    if request.method == 'POST':
        form = BookSearchForm(request.POST)
        if form.is_valid():
            bookname = form.cleaned_data['bookname']
            books = Books.objects.filter(bookname__icontains=bookname)
            if books:
                data['books'] = books  # Add books to data if found
            else:
                data['error'] = 'Книг с названием "%s" не найдено.' % bookname  # Specific message for no results
        else:
            error = 'Форма не заполнена'  # Set error message
            data['error'] = error  # Add error message to data

    else:  # Handling GET requests
        form = BookSearchForm()  # Create a new form for initial display

    # Always add the form to data, regardless of POST success/failure or GET request
    data['form'] = form

    # Return the rendered template with the populated data dictionary
    return render(request, "adm/booksearch.html", data)

#def book_search(request):
#    if request.method == 'POST':
#        form = BookSearchForm(request.POST)
#        if form.is_valid():
#            bookname = form.cleaned_data.get('bookname')
#            # Perform book search
#            books = Books.search_book(bookname)

#            if books:
#                return render(request, 'admin_booksearch', {'books': books})
#            else:
#                return HttpResponse('No books found matching the search criteria.')
#    else:
#        form = BookSearchForm()

    # If the form is not valid or if it's a GET request, render the search form page
#    return render(request, 'admin_booksearch', {'form': form})
