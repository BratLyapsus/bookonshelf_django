from django.contrib import admin
from .models import Writers, Genres, Languages, Books

admin.site.register(Writers)
admin.site.register(Genres)
admin.site.register(Languages)
admin.site.register(Books)