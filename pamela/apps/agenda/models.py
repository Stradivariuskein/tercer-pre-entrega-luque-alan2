from django.db import models
from django.contrib.auth.models import User # user por defecto django
from datetime import datetime, timedelta




class TypeSession(models.Model): # el tipo de sesion q tendra el paciente
    
    remote = models.BooleanField(default=False)
    in_group = models.BooleanField(default=False)
    social_rounds = models.BooleanField(default=False) #obra social si o no
    price = models.IntegerField()
    name = models.CharField(max_length=50, default="nombre")



class Turn(models.Model): # turnos para la sesiones
    date = models.DateField()
    time = models.TimeField()
    time_fin = models.TimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    type_session = models.ForeignKey(TypeSession, on_delete=models.SET_NULL, null=True, blank=True)

    def create_from_strings( user_id, date, time) -> None: # crea el turno con los parametros de tipo str

        if not isinstance(user_id, User):
            user_id= User.objects.get(id=user_id)

        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()

        if isinstance(time, str):
            time = datetime.strptime(time, '%H:%M:%S').time()


        time_fin = datetime.combine(datetime.today(), time) + timedelta(hours=1)

        return Turn(user_id=user_id, date=date, time=time, time_fin=time_fin)

    def __str__(self):
        return f'Turno: {self.date.strftime("%Y-%m-%d")} desde las {self.time} hasta {self.time_fin}'
    
    def day_of_week(self):
        day_number = self.date.weekday()  # Obtener el número del día de la semana (0 = lunes, 6 = domingo)
        days_in_spanish = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return days_in_spanish[day_number]
    
    def month_in_spanish(self): # retorna el mes en español
        month_number = self.date.month
        months_in_spanish = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        return months_in_spanish[month_number - 1]
    
    def get_day(self):
        return self.date.day
    
    def formatted_time(self) -> str: #hora en str
        return f'{self.time.hour}:{self.time.minute}'

    def get_turn(self): # valida y registra un turno en la base de datos
        turns = Turn.objects.all()
        exist_trun = False
        msj = ""
        
        for t in turns:            
            if self.date == t.date and self.time == t.time:
                exist_trun = True
                msj += f"El turno {self.date}, {self.time} esta ocpado\n"

        if not exist_trun:
            new_turn = self.save()
            msj += f"Trueno creado con exito\n{new_turn}"
        return msj
    
    def get_all_turns(self):
        turns = Turn.objects.all()
        return type(turns)




