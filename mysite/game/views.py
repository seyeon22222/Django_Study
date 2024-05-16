from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "game/index.html")

def test(request):
    return render(request, "game/test.html")