from django import forms

from apps.agenda.views import TypeSession, Turn
from .models import HomeFields


class TypeSessionForm(forms.ModelForm):
    name = forms.CharField(label="Nombre", required=True)
    remote = forms.BooleanField(label="Sesión remota", required=False)
    in_group = forms.BooleanField(label="En grupo", required=False)
    social_rounds = forms.BooleanField(label="Obra social", required=False)
    price = forms.IntegerField(label="Precio")
    
    class Meta:
        model = TypeSession
        fields = ['name', 'remote', 'in_group', 'social_rounds', 'price']

class HomeFieldsForm(forms.ModelForm):
    tittle = forms.CharField(label= "Titulo")
    subTittle = forms.CharField(label="Subtitulo")
    faceImg = forms.ImageField(label="Imagen")
    content = forms.CharField(label="Texto")

    class Meta:
        model = HomeFields
        fields = ["tittle", "subTittle", "faceImg", "content"]



class AcountSearchForm(forms.Form):
    name = forms.CharField(max_length=50, label="Nombre")


class TurnForm(forms.ModelForm):
    time = forms.TimeField(label="Hora", widget=forms.DateInput(attrs={'type': 'time'}))
    date = forms.DateField(label="Fecha", widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = Turn
        fields = ["user_id", "time", "date"]  # Agrega "time_fin" al formulario
        

