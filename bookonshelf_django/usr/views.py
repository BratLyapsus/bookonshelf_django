from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from .forms import LoginForm
from books.forms import WritersForm, BooksForm, GenresForm, LanguagesForm, BookSearchForm
from books.models import Writers, Books, Genres, Languages, BorrowedBooks, ReservedBooks, BooksHistory
from django.db.models import Q, F
from main import views as main_views
from main.decorators import has_admin_permission, has_user_permission
from django.contrib import messages  # Import messages
from django.core.exceptions import ObjectDoesNotExist
from .utils import send_notification_email

@has_user_permission
def all_books(request):
    books = Books.objects.filter(is_deleted=False)
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
        try:
            book = Books.objects.get(pk=book_id)
            user = request.user


            # Check if the user has already borrowed the book
            if BorrowedBooks.objects.filter(book=book, user=user).exists():
                messages.warning(request, 'У вас уже есть эта книга.')
                return redirect('user_mybooks')
            #check if dellete_request is present
            if book.deletion_requested or book.is_deleted:
                messages.warning(request, 'Эта книга больше не доступна для заказа.')
                return redirect('user_mybooks')


            if book.bookamount > 0:
                Books.objects.filter(pk=book_id).update(bookamount=F('bookamount') - 1)
                borrowed_book = BorrowedBooks(book=book, user=user)
                borrowed_book.save()
                bookhistory = BooksHistory(book=book, user=user)
                bookhistory.save()

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





def book_reserve(request, book_id):
        try:
            book = Books.objects.get(pk=book_id)
            user = request.user
            if ReservedBooks.objects.filter(book=book, user=user).exists():
                messages.warning(request, 'Вы уже зарезервировали эту книгу.')
                return redirect('user_mybooks')

            # Check if the user has already borrowed the book
            if BorrowedBooks.objects.filter(book=book, user=user).exists():
                messages.warning(request, 'У вас уже есть эта книга.')
                return redirect('user_mybooks')
            if book.deletion_requested or book.is_deleted:
                messages.warning(request, 'Эта книга больше не доступна для заказа.')
                return redirect('user_mybooks')            # Check if the user has already reserved the book


            if book.bookamount == 0:
                reserved_book = ReservedBooks(book=book, user=user)
                reserved_book.save()

                # Use Django's messages framework for consistent messaging
                messages.success(request,
                                 'Вы зарезервировали книгу. Как только она будет доступна, вы сможете ее забрать')

                return redirect('user_mybooks')
            else:
                # Use messages for clear feedback on unavailable books
                messages.warning(request, 'Книга в данный момент доступна, вы можете ее заказать.')

                return redirect('user_bookdetails', book_id=book_id)
        except ObjectDoesNotExist:
            # Handle book not found exception appropriately (e.g., error message)
            messages.error(request, 'Книга не найдена.')  # Error message (Russian)

        return redirect('user_mybooks')  # Redirect back to book details (optional)




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
has_user_permission
def bookshistory(request):
    user = request.user
    bookshistory = BooksHistory.objects.filter(user=user)
    data = {
        'bookshistory': bookshistory,
    }
    return render(request, "usr/bookshistory.html", data)


has_user_permission


def book_return(request, book_id):
    try:
        with transaction.atomic():
            # Get the book from the Books table
            book = Books.objects.get(pk=book_id)

            # Update the bookamount
            Books.objects.filter(pk=book_id).update(bookamount=F('bookamount') + 1)

            # Check if the book is borrowed by the user
            borrowed_book = BorrowedBooks.objects.get(book_id=book_id, user=request.user)

            # Delete the borrowed book entry
            borrowed_book.delete()

            # Display success message
            messages.success(request, 'Книга успешно возвращена.')

            # Check if there are reserved copies of this book
            reserved_books = ReservedBooks.objects.filter(book=book)

            if reserved_books.exists():
                # Get the first reserved book (earliest reservation)
                reserved_book = reserved_books.first()

                # Create a borrowed book entry for the reserved user
                borrowed_book = BorrowedBooks(book=book, user=reserved_book.user)
                borrowed_book.save()

                # Delete the reserved book entry
                reserved_book.delete()

                # Send email notification to the user
                subject = 'Резервирование'
                message = f'Уважаемый {borrowed_book.user.username},\n\nКнига "{book.bookname}" которую вы резервировали, сейчас доступна и вы можете ее забрать.\n\nBest regards,\nС уважением, администрация библиотеки.'
                recipient_list = [borrowed_book.user.email]
                send_notification_email(subject, message, recipient_list)

                # Display a message indicating the book is borrowed by the reserved user
                messages.info(request,
                              f'Книга была автоматически выдана пользователю {borrowed_book.user.username}.')

            # Handle deletion requested books
            if Books.objects.filter(id=book_id, deletion_requested=True).exists():
                book = Books.objects.get(id=book_id)
                book.is_deleted = True
                book.deletion_requested = False
                book.save()

    except ObjectDoesNotExist:
        # Handle the case where the book is not borrowed by the user
        messages.error(request, 'У вас нет этой книги в аренде.')

    # Redirect back to the page displaying borrowed books
    return redirect('user_mybooks')
