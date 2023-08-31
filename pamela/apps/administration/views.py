from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import CreateView, ListView, DeleteView, UpdateView

#agenda imports
from apps.agenda.views import TypeSession, Turn

#login imports
from apps.login.views import Acount

from .forms import TypeSessionForm, AcountSearchForm, HomeFieldsForm, TurnForm

from .models import HomeSection, HomeFields

from my_functions import days_in_spanish
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST



from decorators import ContextMixin

from django.core.exceptions import ObjectDoesNotExist 

from datetime import timedelta

# Create your views here.

@method_decorator(require_POST, name='dispatch')
class TypeSessionCreate(CreateView): # crea un tipo de sesion
    form_class = TypeSessionForm
    model = TypeSession
    #fields = ['remote', 'in_group', 'social_rounds', 'price']
    success_url = reverse_lazy('typeSession')
    template_name = "administration/typeSessionForm.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar datos personalizados al contexto
        context['tittle'] = 'Typo de turno'
        context['boton_name'] = "Crear"
        return context


class TypeSessionUpdate(ContextMixin, UpdateView):
    model = TypeSession
    fields = ['remote', 'in_group', 'social_rounds', 'price']
    template_name = "administration/typeSessionForm.html"
    success_url = reverse_lazy('typeSession')

@method_decorator(require_POST, name='dispatch')
class TypeSessionDelete(ContextMixin, DeleteView):
    model = TypeSession
    success_url = reverse_lazy('typeSession')


def view_typeSession(request): # vista general para ver, editar y borrar todos los tipos de sesion
    context = {
        "typeSession_list": TypeSession.objects.all(),
        "form": TypeSessionForm(),
        "botton_text": "Crear", 
        "tittle": "Typos de sesion"        
               }
    return render(request, "administration/typeSession.html", context)


class AcountListView(ListView): # vista con todas las cuentas existesntes permie editar y borrar.

    model = Acount
    template_name = "administration/listAcounts.html"

    def get_queryset(self): # redeficinmos la query
        queryset = super().get_queryset()

        # Obtener el valor del parámetro de búsqueda desde el formulario
        search_query = self.request.GET.get('name', None) # None es el parametro por defecto si no se le pasa un nombre

        if search_query:
            # Filtrar registros por el campo 'nombre' usando icontains
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar datos personalizados al contexto
        context['form'] = AcountSearchForm()
        context['button_text'] = "Buscar"
        context['tittle'] = "Cuentas"
        return context
    
    def get(self, request, *args, **kwargs):
        # Procesar el formulario de búsqueda
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)
    


@method_decorator(require_POST, name='dispatch')
class AccountDelet(DeleteView): 
    model = Acount
    success_url = reverse_lazy('cuentas')  

class AccountUpdate(ContextMixin, UpdateView):
    model = Acount
    fields = ["id", "email", "name", "lastName", "date", "phone"]
    template_name = 'login/register.html'
    success_url = reverse_lazy('cuentas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar datos personalizados al contexto
        context['button_text'] = "Actualizar"
        return context


@method_decorator(require_POST, name='dispatch')
class HomeUpdate(ContextMixin,UpdateView):
    model = HomeFields
    fields = ['tittle', 'subTittle', 'faceImg', 'content']
    template_name = 'administration/home_form.html'
    success_url = reverse_lazy('home-edit')


class HomeSectionCreate(ContextMixin,CreateView):
    model = HomeSection
    fields = ['tittle', 'subTittle', 'content']
    template_name = 'administration/sectionForm.html'  
    success_url = reverse_lazy('home-edit')
    

class HomeSectionUpdate(ContextMixin,UpdateView):
    model = HomeSection
    fields = ['tittle', 'subTittle', 'content']
    template_name = 'administration/sectionForm.html'  
    success_url = reverse_lazy('home-edit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar datos personalizados al contexto
        context['button_text'] = "Actualizar"
        context['tittle'] = "Modificar seccion"
        return context

@method_decorator(require_POST, name='dispatch')
class HomeSectionDelete(ContextMixin,DeleteView):
    model = HomeSection
    success_url = reverse_lazy('home-edit')



def home_edit(request): # vista para la gestion de home
    context = {
        "tittle": "Editar HOME",
        "tittle2": "Editar Secciones",
        "tittle_form1": "Portada", 
        "form_home_fields": HomeFieldsForm(instance=HomeFields.objects.get(id=1)),
        "tittle_form2": "Seccion",
        "sections": HomeSection.objects.all(),
        'botton_text':'Aceptar'}
    
    return render(request,"administration/home_form.html", context)


class TurnUpdate(ContextMixin, UpdateView):
    model = Turn   
    template_name = 'administration/turnUpdate.html' 
    fields = ["user_id", "time", "date"]
    #form_class =  TurnForm
    success_url = reverse_lazy('admin_turn', kwargs={'p_week': 0})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['user_id'].label = 'Paciente'  # Cambia el label del campo 'user_id'
        form.fields['time'].label = 'Hora'  # Cambia el label del campo 'time'
        form.fields['date'].label = 'Fecha'  # Cambia el label del campo 'date'
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar datos personalizados al contexto
        context['tittle'] = 'Turno'
        context['button_text'] = "Actualizar"
        return context

def turnCreate(request): # funcion especial para crear un turno con mas campos para el administrador
    if request.method == "POST":
        form = TurnForm(request.POST)
        if form.is_valid():
            # Obtenemos los datos del formulario
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            user_id = form.cleaned_data['user_id']
            
            # Calculamos time_fin como una hora después de time
            time_fin = (datetime.combine(date, time) + timedelta(hours=1)).time()
            type_session = Acount.objects.get(user_id=user_id).type_session
            # Creamos el objeto Turn y lo guardamos
            new_turn = Turn(date=date, time=time, time_fin=time_fin, user_id=user_id, type_session=type_session)
            new_turn.save()

            return redirect(reverse_lazy('admin_turn', kwargs={'p_week': 0}))  # Cambia a la URL correcta

    else:
        form = TurnForm()

    return render(request, 'administration/turnCreate.html', {'form': form})


def admin_turn(request, p_week): # muestra por semnas todos los turnos agendados
    try:
        turns = Turn.objects.all()
        turnsAndDays = []

    except ObjectDoesNotExist:
        return render(request, 'administration/turns.html', {'turns': []})

    current_week_number = datetime.now().isocalendar()[1] + p_week

    week= {}
    for day in days_in_spanish:
        week[day] = []

    for turn in turns:
        account = Acount.objects.get(user_id=turn.user_id)
        day_of_week = turn.day_of_week()  # 0: lunes, 1: martes, ..., 6: domingo

        # Crea una estructura para almacenar los turnos por semana y día
        week_number = turn.date.isocalendar()[1]  # Número de semana del año

        if week_number == current_week_number:
            week[day_of_week].append([f"{turn.time}", f"{turn.date}", f"{account.lastName}, {account.name}", account.phone, turn.day_of_week(), turn.id])

    context = {'week': week,
               'form': TurnForm(),
               'tittle': "Administrar Turnos",
               'button_text': 'Crear +',
               'next_week': p_week+1}
    if not p_week == 0: # la semana 0 es la semana actual
        context['previus_week'] = p_week - 1


    

    return render(request, 'administration/turns.html', context)




