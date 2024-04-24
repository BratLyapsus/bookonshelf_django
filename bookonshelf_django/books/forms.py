from django import forms
from .models import Books, Writers, Genres, Languages
from django.forms import ModelForm



class WritersForm(ModelForm):
    class Meta:
        model = Writers
        fields = ['writername']
        widgets = {
            'writername': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Автор'
            }),
        }

class GenresForm(ModelForm):
        class Meta:
            model = Genres
            fields = ['genre']
            widgets = {
                'genre': forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Жанр'
                }),
            }

class LanguagesForm(ModelForm):
    class Meta:
        model = Languages
        fields = ['language']
        widgets = {
            'language': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Язык'
            }),
        }


class BooksForm(forms.ModelForm):
    writer = forms.ModelChoiceField(queryset=Writers.objects.all(),
                                    empty_label='Выберите автора',
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    genre = forms.ModelChoiceField(queryset=Genres.objects.all(),
                                   empty_label='Выберите жанр',
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    language = forms.ModelChoiceField(queryset=Languages.objects.all(),
                                      empty_label='Выберите язык',
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Books
        fields = ['bookname', 'writer', 'genre', 'language', 'pageamount', 'bookamount', 'registrationnumber', 'bookannotation', 'cover']
        widgets = {
            'bookname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название книги'
            }),
            'pageamount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество страниц'
            }),
            'bookamount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество книг'
            }),
            'registrationnumber': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Регистрационный номер'
            }),
            'bookannotation': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Аннотация'
            }),
            'cover': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
        }

class BookSearchForm(forms.Form):
    bookname = forms.CharField(
        label='bookname',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название книги'})
    )
#    writername = forms.CharField(
#        label='writername',
#        max_length=50,
#        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Автор'})
#    )

#    def clean(self):
#        cleaned_data = super().clean()
#        bookname = cleaned_data.get('bookname')
#        writername = cleaned_data.get('writername')

#        if not bookname and not writername:
#            raise forms.ValidationError("Заполните одно из полей поиска")

#        return cleaned_data

