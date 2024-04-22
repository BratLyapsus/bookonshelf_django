from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def has_admin_permission(view_func):
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.groups.filter(name='admin').exists():
            return redirect('no_access')
        return view_func(request, *args, **kwargs)
    return decorator

def has_user_permission(view_func):
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.groups.filter(name='user').exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('no_access')
    return decorator

