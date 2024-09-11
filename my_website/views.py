from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about_me.html')

def skills(request):
    return render(request, 'skills.html')

def projects(request):
    return render(request, 'projects.html')

def contact(request):
    return render(request, 'contact.html')

def lyme_disease(request):
    return render(request, 'lyme_disease.html')

def bells_palsy(request):
    return render(request, 'bells_palsy.html')

def website_info(request):
    return render(request, 'website_info.html')