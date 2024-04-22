from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from adm import views as adm_views
from main.decorators import has_admin_permission, has_user_permission


def index(request):
    from django.contrib.auth.models import Group
    user_is_admin = request.user.groups.filter(name='admin').exists()
    return render(request, "main/index.html", {'title': 'Главная страница', 'user_is_admin': user_is_admin})

def info(request):
    return render(request, "main/info.html", {'title': 'Информация'})

def no_access(request):
    return render(request, "main/no_access.html", {'title': 'Доступ запрещен'})


def login_view(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Create form with POST data
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='admin').exists():
                    #print('user is admin')
                    return redirect('admin_home')  # Redirect to admin home page (typo fix)
                else:
                    #print('user is usr')
                    return redirect('user_home')  # Redirect to regular user home page (typo fix)
            else:
                form = LoginForm()
                data = {
                    'title': 'Вход на личную страницу', 
                    'error_message': 'Неправильное имя пользователя или пароль', 
                    'form': form}
                return render(request, "main/login.html", data)
    else:
        form = LoginForm()  # Create an empty form for GET requests
        data = {'title': 'Вход на личную страницу', 'form': form}
        return render(request, "main/login.html", data)


def logout_view(request):
   logout(request)
   return redirect('home')

#def has_admin_permission(view_func):
#    def decorator(request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            return redirect('login')

#        if not request.user.groups.filter(name='admin').exists():
#            return redirect('no_access')#('permission_denied')
#        return view_func(request, *args, **kwargs)
#    return decorator

#def has_user_permission(view_func):
#    def decorator(request, *args, **kwargs):
#        if not request.user.is_authenticated:
#            return redirect('login')

#        if request.user.groups.filter(name='user').exists():
#            return view_func(request, *args, **kwargs)
#        else:
#            print('no_access')
#            return redirect('no_access')
#    return decorator

@has_user_permission
def user_home(request):    
    return render(request, 'main/user_home.html')

@has_admin_permission
def admin_home(request):    
    return render(request, 'main/admin_home.html')
   