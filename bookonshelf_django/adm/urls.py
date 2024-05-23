
from django.urls import path
from . import views

urlpatterns = [
    path('adm/allbooks', views.all_books, name='admin_allbooks'),
    path('adm/archivebooks', views.archive_books, name='admin_archivebooks'),
    path('adm/addbook', views.add_book, name='admin_addbooks'),
    path('adm/addwriter', views.add_writer, name='admin_addwriter'),
    path('adm/addgenre', views.add_genre, name='admin_addgenre'),
    path('adm/addlanguage', views.add_language, name='admin_addlanguage'),
    path('adm/booksearch', views.book_search, name='admin_booksearch'),
    path('adm/books/<int:book_id>/', views.book_details, name='admin_bookdetails'),
    path('adm/deletebook/<int:book_id>/', views.book_delete, name='admin_deletebook'),
    path('adm/restorebook/<int:book_id>/', views.book_restore, name='admin_restorebook'),
    path('adm/editbook/<int:book_id>/', views.book_edit, name='admin_editbook'),
]
