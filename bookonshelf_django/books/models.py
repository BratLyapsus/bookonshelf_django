from django.db import models

#class Books(models.Model):    
#    writer_id = models.IntegerField('writerid')
#    genre_id = models.IntegerField('genreid')
#    language_id = models.IntegerField('languageid')
#    bookname = models.CharField('bookName', max_length=250 )
#    bookannotation = models.TextField('bookAnnotation')
#    pageamount = models.IntegerField('pageAmount')
#    bookamount = models.IntegerField('bookAmount')
#    registrationnumber = models.CharField('registrationNumber', max_length=10 )
    
#class Users(models.Model):    
    
#    username = models.CharField('username', max_length=20)
#    password = models.CharField('password', max_length=20)
#    firstname = models.CharField('firstname', max_length=20, default='John')
#    lastname = models.CharField('lastname', max_length=20, default='Baker')
#    useremail = models.EmailField('email', default='exampl@exampli.com')

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
        
