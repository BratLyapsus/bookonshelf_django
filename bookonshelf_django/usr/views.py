from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
#from .forms import LoginForm
from books.forms import WritersForm, BooksForm, GenresForm, LanguagesForm, BookSearchForm
from books.models import Writers, Books, Genres, Languages, BorrowedBooks
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

@has_user_permission
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
    return render(request, "usr/booksearch.html", data)

@has_user_permission
def book_details(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    return render(request, 'usr/bookdetails.html', {'book': book})

@has_user_permission
def book_borrow(book_id, user_id):
    try:
        with transaction.atomic():
            book = Books.objects.select_for_update().get(id=book_id)
            if book.bookamount > 0:
                borrowed_book = BorrowedBooks.objects.create(book=book, user_id=user_id)
                book.bookamount -= 1
                book.save()
                # Commit the transaction explicitly
                transaction.commit()
                return borrowed_book
            else:
                # If book is not available, raise an exception with a descriptive message
                raise Exception("Book is not available for borrowing")
    except Books.DoesNotExist:
        return None  # Book does not exist
    except Exception as e:
        # Rollback the transaction in case of any exception
        transaction.rollback()
        raise e  # Re-raise the exception for further handling

has_user_permission
def mybooks(request):
    mybooks = BorrowedBooks.objects.all()
    data = {
        'mybooks': mybooks,
    }
    return render(request, "usr/mybooks.html", data)