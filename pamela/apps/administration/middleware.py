from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.login.models import Acount


class AdminOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            
            try:
                account = Acount.objects.get(user_id=request.user.id)
                
                
                if not account.is_admin and request.path_info.startswith('/administration/'):
                    # Bloquear solo si el usuario no es administrador y está en una ruta de /administration
                    return redirect(reverse_lazy('turns'))  # Redirige a la página de turnos
            except Acount.DoesNotExist:
                #return HttpResponse(request.path_info)
                return redirect(reverse_lazy('register'))
                
        response = self.get_response(request)
        return response
