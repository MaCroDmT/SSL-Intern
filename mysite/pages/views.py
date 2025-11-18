from django.shortcuts import render # <--- This tool helps load files
from django.http import HttpResponse

def home(request):
    # Instead of returning text, we "render" (load) the file
    return render(request, 'home.html')

def contact(request):
    return HttpResponse("<h1>Contact Page: Email us at sonia@sweaters.com</h1>")