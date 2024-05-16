from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
#from .forms import LoginForm
from books.forms import WritersForm, BooksForm, GenresForm, LanguagesForm, BookSearchForm
from books.models import Writers, Books, Genres, Languages
from django.db.models import Q
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
            bookname = booksform.cleaned_data['bookname']
            writername = booksform.cleaned_data['writer']
            if Books.objects.filter(bookname=bookname, writer=writername).exists():
                error = 'Такая книга уже существует'
            else:
                booksform.save()
                return redirect('admin_allbooks')
        else:
            error = 'Форма заполнена неверно'
    else:
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
            writer_name = writersform.cleaned_data['writername']
            # Check if a writer with the same name already exists
            if Writers.objects.filter(writername=writer_name).exists():
                error = 'Такой писатель уже существует.'
            else:
                writersform.save()
                return redirect('admin_addbooks')
        else:
            error = 'Форма заполнена неверно'
    else:
        writersform = WritersForm()

    data = {
        'writersform': writersform,
        'error': error
    }
    return render(request, "adm/addwriter.html", data)

@has_admin_permission
def add_genre(request):
    error = ''
    if request.method == 'POST':
        genresform = GenresForm(request.POST)
        if genresform.is_valid():
            genre = genresform.cleaned_data['genre']
            if Genres.objects.filter(genre=genre).exists():
                error = 'Такой жанр уже существует'
            else:
                genresform.save()
                return redirect('admin_addbooks')
        else:
            error = 'Форма заполнена неверно'
    genresform = GenresForm()

    data = {

        'genresform': genresform,
        'error': error

    }
    return render(request, "adm/addgenre.html", data)

@has_admin_permission
def add_language(request):
    error = ''
    if request.method == 'POST':
        languagesform = LanguagesForm(request.POST)
        if languagesform.is_valid():  # Validate the form
            language = languagesform.cleaned_data['language']
            if Languages.objects.filter(language=language).exists():
                error = 'Такой язык уже существует'
            else:
                languagesform.save()
                return redirect('admin_addbooks')
        else:
            error = 'Форма заполнена неверно'
    else:
        languagesform = LanguagesForm()

    data = {
        'languagesform': languagesform,
        'error': error
    }
    return render(request, "adm/addlanguage.html", data)
@has_admin_permission
def book_details(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    return render(request, 'adm/bookdetails.html', {'book': book})

@has_admin_permission
def book_search(request):
    data = {}  # Initialize empty data dictionary
    error = ''

    if request.method == 'POST':
        form = BookSearchForm(request.POST)
        if form.is_valid():
            #bookname = form.cleaned_data['bookname']
            query = form.cleaned_data['query']
            #books = Books.objects.filter(bookname__icontains=bookname)
            books = Books.search(query)
            if books:
                data['books'] = books  # Add books to data if found
                form = BookSearchForm()  # Create a new form for initial display
            else:
                data['error'] = 'Книг с запросом "%s" не найдено.' % query  # Specific message for no results
        else:
            error = 'Форма не заполнена'  # Set error message
            data['error'] = error  # Add error message to data

    else:  # Handling GET requests
        form = BookSearchForm()  # Create a new form for initial display

    # Always add the form to data, regardless of POST success/failure or GET request
    data['form'] = form

    # Return the rendered template with the populated data dictionary
    return render(request, "adm/booksearch.html", data)

@has_admin_permission
def book_delete(request, book_id):
    # Step 1: Retrieve the book object using book_id
    book = get_object_or_404(Books, id=book_id)

    # Step 2: Delete the retrieved book object
    book.delete()

    # Step 3: Redirect to a new page or render a template
    return redirect('admin_allbooks')  # Redirect to a specific URL

@has_admin_permission
def book_edit(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    error = ''
    if request.method == 'POST':
        booksform = BooksForm(request.POST, request.FILES, instance=book)
        if booksform.is_valid():
            booksform.save()
            return redirect('admin_allbooks')
        else:
            error = 'Форма заполнена неверно'
    booksform = BooksForm(instance=book)

    data = {

        'booksform': booksform,
        'error': error

    }
    return render(request, 'adm/editbook.html', {'booksform': booksform, 'error': error})