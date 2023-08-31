from django.db import models
from django.contrib.auth.models import User
from apps.agenda.models import TypeSession



# Create your models here.
class Acount(models.Model): # acount esta vinculado con lo usuario de django
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    type_session = models.ForeignKey(TypeSession, on_delete=models.PROTECT, default=3)
    email = models.EmailField(unique=True) # se inicia sesion con el email
    imgAvatar = models.ImageField(default="avatares/avatar.png", upload_to="avatares/")
    name = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    date = models.DateField() # fecha de nacimiento    
    phone = models.CharField(max_length=16)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}, {self.email}, {self.name}, {self.lastName}, {self.date}, {self.phone}, {self.is_admin}"







    