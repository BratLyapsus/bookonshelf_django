﻿from django.db import models

class Writers(models.Model):
    writername = models.CharField('writername', max_length=20)
  
    def __str__(self):
        return self.writername

    class Meta:
        verbose_name = 'Писатель'
        verbose_name_plural = 'Писатели'
        
class Genres(models.Model):
    genre = models.CharField('genre', max_length=20)
  
    def __str__(self):
        return self.genre

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        
class Languages(models.Model):
    language = models.CharField('language', max_length=20)
  
    def __str__(self):
        return self.language

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

class Books(models.Model):

    bookname = models.CharField('bookName', max_length=250 )
    bookannotation = models.TextField('bookAnnotation')
    pageamount = models.IntegerField('pageAmount')
    bookamount = models.IntegerField('bookAmount')
    registrationnumber = models.CharField('registrationNumber', max_length=10 )
    writer = models.ForeignKey(Writers, on_delete=models.CASCADE)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='cover/', blank=True)

    def __str__(self):
        return self.bookname

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        
