from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from .forms import LoginForm
from books.forms import WritersForm, BooksForm, GenresForm, LanguagesForm, BookSearchForm
from books.models import Writers, Books, Genres, Languages, BorrowedBooks, ReservedBooks
from django.db.models import Q, F
from main import views as main_views
from main.decorators import has_admin_permission, has_user_permission
from django.contrib import messages  # Import messages

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


def book_borrow(request, book_id):
    if request.method == 'POST':
        try:
            book = Books.objects.get(pk=book_id)
            user = request.user

            if book.bookamount > 0:
                Books.objects.filter(pk=book_id).update(bookamount=F('bookamount') - 1)
                borrowed_book = BorrowedBooks(book=book, user=user)
                borrowed_book.save()

                # Use Django's messages framework for consistent messaging
                messages.success(request, 'Книга готова. Вы можете ее забрать.')

                return redirect('user_mybooks')
            else:
                # Use messages for clear feedback on unavailable books
                messages.warning(request, 'Книга в данный момент недоступна.')

                return redirect('user_bookdetails', book_id=book_id)
        except ObjectDoesNotExist:
            # Handle book not found exception appropriately (e.g., error message)
            messages.error(request, 'Книга не найдена.')  # Error message (Russian)

        return redirect('user_mybooks')  # Redirect back to book details (optional)

    else:
        return redirect('user_bookdetails', book_id=book_id)  # Redirect on non-POST requests


def book_reserve(book_id, user_id):
    return redirect('user_mybooks')

has_user_permission
def mybooks(request):
    user = request.user
    borrowedbooks = BorrowedBooks.objects.filter(user=user)
    reservedbooks = ReservedBooks.objects.filter(user=user)
    data = {
        'borrowedbooks': borrowedbooks,
        'reservedbooks': reservedbooks,
    }
    return render(request, "usr/mybooks.html", data)