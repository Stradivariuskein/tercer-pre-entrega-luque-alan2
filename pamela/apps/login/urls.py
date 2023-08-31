from django.urls import path, include
from .views import *
from decorators import add_general_context

urlpatterns = [
    path('login/', add_general_context(view_login), name= "login"),
    path('register/', add_general_context(Register.as_view()), name= "register"),
    path('register/acount/', add_general_context(register_acount), name= "acount"),
    path('logout/', add_general_context(user_logout), name= "logout"),
]
    
