from django.shortcuts import render
from apps.administration.models import HomeSection

# Create your views here.

def home(request):
    sections = HomeSection.objects.all()
    context = {"sections": sections}
    return render(request, "home/home.html", context)


def curriculum(request):
    return render(request, 'home/curriculum.html')