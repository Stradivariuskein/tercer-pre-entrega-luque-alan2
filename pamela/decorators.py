from apps.login.models import Acount
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy

class ContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        account = Acount.objects.get(user=user)
        context['botton_text'] = 'Aceptar'
        context['imgAvatar'] = account.imgAvatar
        return context

def is_admin_decorator(function): # valida si una cuenta es admin

    @login_required
    def custom_function(request, *args, **kwargs):
        try:
            acount = Acount.objects.get(user_id=request.user)
            request.is_admin = acount.is_admin
            
        except:    
            request.is_admin = False

        return function(request, *args, **kwargs)

       
    return custom_function

def admin_only(function):
    @is_admin_decorator
    def custom_function(request, *args, **kwargs):
        if request.is_admin:
            return function(request, *args, **kwargs)
        return redirect(reverse_lazy('turns'))
    return custom_function

def add_general_context(function): # valida si una cuenta es admin

    def custom_function(request, *args, **kwargs):
        try:
            acount = Acount.objects.get(user_id=request.user)
            request.imgAvatar = acount.imgAvatar
            request.is_admin = acount.is_admin
            
        except:    
            request.imgAvatar = "avatares/avatar.png"
            request.is_admin = False

        return function(request, *args, **kwargs)
    
    return custom_function

def valid_acount(function):
    @login_required
    def custom_function(request, *args, **kwargs): # valida si un usuario tiene cuenta

        try:
            account = Acount.objects.get(user_id=request.user) 
            return function(request, *args, **kwargs)
        except Acount.DoesNotExist:
            return redirect(reverse_lazy('acount'))


    return custom_function