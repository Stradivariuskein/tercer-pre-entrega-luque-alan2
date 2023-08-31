from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist  # Importa la excepción necesaria

from datetime import datetime, timedelta

from django.views.generic import DeleteView

from decorators import ContextMixin

# My models
from .models import *
from .forms import *

from apps.login.models import Acount
from apps.login.forms import AcountForm


# Create your views here.



def get_turn(request): # confirmacion para recervar el turno
    #if not valid_acount(request):
    #    return redirect('/login')
    content = {}
    if request.method == "POST":
        content["button_text"] = "Aceptar"
        data = request.POST.copy()

        if data:            
            #convertirmos el turno a tipo turn
            new_turn = data["turn"].split()

            new_turn = Turn.create_from_strings(date=new_turn[1], time=new_turn[4], user_id=request.user.id)

            if isinstance(new_turn, Turn):
                
                new_turn.get_turn()

                content["turn"] =  new_turn
                content["day_week"] = new_turn.day_of_week()                
                content["day"] = new_turn.get_day()
                content["month"] = new_turn.month_in_spanish()
                content["time"] = new_turn.formatted_time()
                content["msj"] = "Quiere tomar el turno?"
                return render(request, 'agenda/get_turn.html', content)
                
            else:
                return HttpResponse(f'===== Error no es instacia {new_turn} =====')
        else:
            return HttpResponse("===== Error empty data =====")
    elif request.method == "GET":
        content["button_text"] = "Tomar turno"
    return render(request, 'agenda/get_turn.html', content)


def turnCreate(reuqest): # crea el turno y lo guarda en la base de datos

    if reuqest.method == "POST":
        data = reuqest.POST


        if data:
            turn_str = data["turn"].split()
            fecha = turn_str[1]
            hour = turn_str[4]

            if not Turn.objects.get(date=fecha,time=hour).DoesNotExist: # valida el turno
                new_turn = Turn.create_from_strings(user_id=reuqest.user, date=fecha, time=hour)
                new_turn.save()
            
            return redirect(reverse_lazy("turns"))
    return redirect(reverse_lazy("getTurn"))



def turnos_disponibles(request): # genera una lista de turnos disponibles teniendo en cuenta los q estan reservados
    if request.is_admin:
        return redirect(reverse_lazy('admin_turn', kwargs={'p_week': 0}))

    context = {"button_text": "Buscar"}
    context["tittle"] = "Turnos disponibles"
    context['boton_name'] = "Buscar"


    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        
        context["search_form"] = search_form

        if search_form.cleaned_data['day_of_week']:
            day_search = [search_form.cleaned_data['day_of_week']]
        else:
            day_search = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

        if search_form.cleaned_data['date']:
            fecha_init = search_form.cleaned_data['date']
            fecha_init = datetime.combine(fecha_init, datetime.min.time())
        else:
            fecha_init = datetime.now()
        
        if not (search_form.cleaned_data['date'] and search_form.cleaned_data['day_of_week']):
            search_form = SearchForm()
            context["search_form"] = search_form

    else:
        search_form = SearchForm()
        context["search_form"] = search_form
        fecha_init = datetime.now()
        day_search = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

    #  lo q hago a continuacion es generar los turnos posibles para mostrarlos
    # se calculan cada 1 hora y como maximo son 3 meses desde la fecha actual para resevar turno

    #  guardamos el valo para hacer la busqueda
    #
    fecha_init = fecha_init.replace(hour=0, minute=0, second=0, microsecond=0)
    fecha_init = datetime.combine(fecha_init, datetime.min.time())
    
    fecha_search = fecha_init
   
    #=================================================
    #esto puede ir en una funcion
    #================================================= 
    
    # Calcular la fecha final (3 meses desde la fecha actual)
    fecha_fin = fecha_init + timedelta(days=90)

    # Generar la lista de horarios disponibles cada 1 hora
    horarios_disponibles = []
    fecha_init += timedelta(hours=9)
    


    for i in range(0,89):
        
        for j in range(0,12):
            horarios_disponibles.append(fecha_init)
            fecha_init += timedelta(hours=1)
            
        if fecha_init.hour >= 21:
                fecha_init += timedelta(days=1)
                fecha_init = fecha_init.replace(hour=0, minute=0, second=0, microsecond=0)

        fecha_init += timedelta(hours=9)

    

    # Obtener los turnos ocupados en el rango de fechas
    turnos_ocupados = Turn.objects.filter(date__range=[horarios_disponibles[0], fecha_fin])

    week_days = []
    horarios_libres = []
    i=0
    for hora in horarios_disponibles:
        fecha = hora  # Obtener la fecha
        temp_turn = Turn(date=fecha)
        day_str = temp_turn.day_of_week()

        if fecha > fecha_search and day_str in day_search: # validacion de la busqueda
            hora_del_dia = hora.time()  # Obtener la hora del día
            

            # Verificar si el turno para esta fecha y hora ya está ocupado
            if not turnos_ocupados.filter(date=fecha, time=hora_del_dia).exists():
                hora_fin = (hora + timedelta(hours=1)).time()

                new_turn = Turn(date=fecha, time=hora_del_dia, time_fin=hora_fin,user_id=request.user)
                horarios_libres.append(new_turn)
                week_days.append(new_turn.day_of_week())
        i +=1

    horarios_libres = zip(horarios_libres, week_days)
    context['turns'] = horarios_libres

    
    return render(request, 'agenda/turnos_disponibles.html', context)


def perfil(request): # eidicion del perfil de usuario actual
      
    context = {
        "tittle": "Perfil",
        "boton_name": "Actualizar",
    }
    
    if request.method == "GET":
        account = Acount.objects.get(user=request.user)
        sessions = TypeSession.objects.all()
        session_choices = []
        for session in sessions:
            session_choices.append((session, session.name))
        form = AcountForm(instance=account)  # Inicializa el formulario con la instancia
        form.fields['typeSession'].choices = session_choices
        context["form"] = form
    elif request.method == "POST":
        account = Acount.objects.get(user=request.user)
        form = AcountForm(data=request.POST, files=request.FILES, instance=account)  # Pasa la instancia para actualizar

        if form.is_valid():

            form.save()  # Guarda los cambios en la base de datos
            return redirect(reverse_lazy("perfil"))  # Redirige a la página del perfil actualizado
    
        context["form"] = form

    
    return render(request, "agenda/perfil.html", context)


class TurnDelete(ContextMixin, DeleteView): #elimina un turno
    model = Turn
    success_url = reverse_lazy('my-turns')


def my_turns(request): # muestra todos los turnos reservados
    if request.is_admin:
        return redirect(reverse_lazy('admin_turn', kwargs={'p_week': 0}))

    try:
        turns = Turn.objects.filter(user_id=request.user)
        turnsAndDays = []

    except ObjectDoesNotExist:
        return render(request, 'agenda/my_turns.html', {'turns': []})


    try:
        for turn in turns:


            turnsAndDays.append((turn, turn.day_of_week()))
        context = {'turns': turnsAndDays}
    except:
        context = {'turns': [(turns, turns.day_of_week())]}


    return render(request, 'agenda/my_turns.html', context)





