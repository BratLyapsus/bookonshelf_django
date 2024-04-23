#from csv import writer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
#from .forms import LoginForm
from books.forms import WritersForm
from books.models import Writers
from main import views as main_views
from main.decorators import has_admin_permission, has_user_permission

@has_admin_permission
def all_books(request):
    writers = Writers.objects.all()
    return render(request, "adm/allbooks.html", {'writers': writers})

#def add_book(request):
#    writersform = WritersForm()
#    data = {
#        'writersform': writersform
#        }
#    return render(request, 'adm/addbook.html', data)

def add_book(request):
    error = ''
    if request.method == 'POST':
        writersform = WritersForm(request.POST)
        if writersform.is_valid():
            writersform.save()
            return redirect('admin_allbooks') 
        else: 
            error = 'Форма заполнена неверно'
    writersform = WritersForm()
    
    data = {
        
        'writersform': writersform,
        'error': error
        
        } 
    return render(request, "adm/addbook.html", data)


def add_writer(request):
    error = ''
    if request.method == 'POST':
        writersform = WritersForm(request.POST)
        if writersform.is_valid():
            writersform.save()
            return redirect('admin_allbooks')
        else:
            error = 'Форма заполнена неверно'
    writersform = WritersForm()

    data = {

        'writersform': writersform,
        'error': error

    }
    return render(request, "adm/addwriter.html", data)