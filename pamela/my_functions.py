from django.http import HttpResponse
from apps.login.models import Acount
from apps.agenda.models import Turn
from apps.agenda.forms import SearchForm

days_in_spanish = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

def valid_acount(request):
    if request.user.is_authenticated:
        try:
            user = Acount.objects.get(user_id=request.user) # Suponiendo que tienes una relación OneToOneField llamada 'acount' en tu modelo User
        except Acount.DoesNotExist:
            return False
    else:
        return False
    return True

def search_turn(request):
    form = SearchForm(request.GET)
    turns = Turn.objects.all()

    if form.is_valid():
        day_of_week = form.cleaned_data['day_of_week']
        date = form.cleaned_data['date']

        if day_of_week:
            turns = turns.filter(date__week_day=SearchForm.day_choices.index(day_of_week))

        if date:
            turns = turns.filter(date=date)

    return turns


from django.utils.decorators import method_decorator

def add_context_to_view(context, my_context):
    """
    Decorador que agrega un contexto adicional a una vista.
    
    Args:
        context (dict): El contexto adicional a agregar.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            extra_context = context.copy()
            extra_context.update(my_context)
            return HttpResponse(extra_context)
            return view_func(request, *args, **extra_context)
        return _wrapped_view
    return decorator