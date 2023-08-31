from django import forms
from .models import TypeSession
from apps.login.models import Acount

class SearchForm(forms.Form):
    day_choices = [
        ('', 'Seleccione un día'),
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]
    
    day_of_week = forms.ChoiceField(label="Dia",choices=day_choices, required=False)
    date = forms.DateField(label="Desde", required=False, widget=forms.DateInput(attrs={'type': 'date'}))








