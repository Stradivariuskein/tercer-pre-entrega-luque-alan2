from django.urls import path, include
from .views import *
from decorators import add_general_context

urlpatterns = [
    path('', add_general_context(home), name='home' ),
    path('curriculum', add_general_context(curriculum), name='curriculum' ),
]