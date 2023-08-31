from django.urls import path, include
from .views import *
from decorators import add_general_context, valid_acount


urlpatterns = [
    path('getTurn/', valid_acount(add_general_context(get_turn)), name= "getTurn"),
    path('turnCreate', valid_acount(add_general_context(turnCreate)), name= "turnCreate"),
    
    path('turnos/', valid_acount(add_general_context(turnos_disponibles)), name= "turns"),
    path('my_turns/', valid_acount(add_general_context(my_turns)), name= "my-turns"),
    path('delet_turn/<int:pk>/', valid_acount(add_general_context(TurnDelete.as_view())), name= "delet_turn"),

    path('perfil/', valid_acount(add_general_context(perfil)), name= "perfil"),
    

]
