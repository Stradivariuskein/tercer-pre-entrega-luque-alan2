from .models import Acount
from django import forms
from django.contrib.auth.models import User # user por defecto django
from apps.agenda.models import TypeSession


class AcountForm(forms.ModelForm):
    sessions = TypeSession.objects.all()
    session_choices = []
    for session in sessions:
        session_choices.append((session, session.name))
        
    
    typeSession = forms.ChoiceField(label="Tipo de sesion",choices=session_choices, required=True)
    email = forms.EmailField(label="Email") # se inicia sesion con el email
    imgAvatar = forms.ImageField(label="Avatar", required=False)
    name = forms.CharField(label="Nombre")
    lastName = forms.CharField(label="Apellido")
    date = forms.DateField(label="Fecha de nacimiento") # fecha de nacimiento    
    phone = forms.CharField(label="Numero de telefono")
    class Meta:
        model = Acount
        fields = ('email', 'name', 'lastName', 'date', 'phone', 'imgAvatar')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Usar PasswordInput para ocultar la contraseña

    class Meta:
        model = User
        fields = ('email', 'password')


