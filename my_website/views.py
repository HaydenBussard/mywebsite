from django.shortcuts import render

def home(request):
    return render(request, 'about_me.html')

def skills(request):
    return render(request, 'skills.html')

def projects(request):
    return render(request, 'projects.html')

def contact(request):
    return render(request, 'contact.html')