from django.contrib import admin
from .models import Writers, Genres, Languages, Books, BorrowedBooks, ReservedBooks

admin.site.register(Writers)
admin.site.register(Genres)
admin.site.register(Languages)
admin.site.register(Books)
admin.site.register(BorrowedBooks)
admin.site.register(ReservedBooks)