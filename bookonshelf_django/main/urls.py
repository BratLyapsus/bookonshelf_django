
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('info', views.info, name='info'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('no_access', views.no_access, name='no_access'),
    path('admin_home', views.admin_home, name='admin_home'),
    path('user_home', views.user_home, name='user_home'),
    ]
