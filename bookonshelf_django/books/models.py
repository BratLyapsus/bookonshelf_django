from django.db import models
from django.contrib.auth.models import User

class Writers(models.Model):
    writername = models.CharField('writername', max_length=50)
  
    def __str__(self):
        return self.writername

    class Meta:
        verbose_name = 'Писатель'
        verbose_name_plural = 'Писатели'
        
class Genres(models.Model):
    genre = models.CharField('genre', max_length=50)
  
    def __str__(self):
        return self.genre

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        
class Languages(models.Model):
    language = models.CharField('language', max_length=50)
  
    def __str__(self):
        return self.language

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

class Books(models.Model):

    bookname = models.CharField('bookName', max_length=50 )
    bookannotation = models.TextField('bookAnnotation')
    pageamount = models.IntegerField('pageAmount')
    bookamount = models.IntegerField('bookAmount')
    registrationnumber = models.CharField('registrationNumber', max_length=10 )
    writer = models.ForeignKey(Writers, on_delete=models.CASCADE)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='cover/', blank=True)

    @classmethod
    def search(cls, query):
        return cls.objects.filter(
            models.Q(bookname__icontains=query) |
            models.Q(registrationnumber__icontains=query) |
            models.Q(writer__writername__icontains=query) |
            models.Q(genre__genre__icontains=query)
        )

    def __str__(self):
        return self.bookname

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class BorrowedBooks(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        #return self.registrationnumber
        return str(self.book.bookname)

    class Meta:
        verbose_name = 'Книги у вас'
        verbose_name_plural = 'Книги у вас'

class ReservedBooks(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        #return self.registrationnumber
        return str(self.book.bookname)

    class Meta:
        verbose_name = 'Зарезервированная книга'
        verbose_name_plural = 'Зарезервированные книги'


