from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django import forms
from captcha.widgets import ReCaptchaV3
from captcha.fields import ReCaptchaField
import requests
from django.conf import settings
from django.shortcuts import render
from .models import PortfolioPage, ResumeVersion, HomePage, SkillCategory, SkillsPageContent, BeyondWorkSection, BeyondWorkPageContent

def home(request):
    page = HomePage.objects.first()
    return render(request, 'home.html', {
        'page': page
    })

# def about(request):
#     return render(request, 'about_me.html')

def about(request):
    page = PortfolioPage.objects.first()
    resumes = ResumeVersion.objects.all()
    # Add absolute URLs for all resumes
    for resume in resumes:
        resume.absolute_url = request.build_absolute_uri(resume.file.url)
    return render(request, 'about_me.html', {
        'page': page,
        'resumes': resumes,
    })

def skills(request):
    # 1. Fetch the singleton page content (or create it if it doesn't exist)
    page_content, created = SkillsPageContent.objects.get_or_create(pk=1)
    
    # 2. Retrieve all skill categories
    skill_categories = SkillCategory.objects.all().prefetch_related('skills')

    context = {
        'page': page_content, # Pass the content object to the template
        'skill_categories': skill_categories,
    }
    return render(request, 'skills.html', context)

def projects(request):
    return render(request, 'projects.html')

def lyme_disease(request):
    return render(request, 'lyme_disease.html')

def bells_palsy(request):
    return render(request, 'bells_palsy.html')

def website_info(request):
    return render(request, 'website_info.html')

def health_resources(request):
    return render(request, 'health_resources.html')

def beyond_engineering(request): # Assuming this is your view function name based on your 'about_me.html'
    # 1. Fetch the singleton page content
    page_content, created = BeyondWorkPageContent.objects.get_or_create(pk=1)
    
    # 2. Retrieve all sections, prefetching details for efficiency
    sections = BeyondWorkSection.objects.all().prefetch_related('details')

    context = {
        'page': page_content,
        'sections': sections,
    }
    return render(request, 'beyond_engineering.html', context)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    def clean(self):
        cleaned_data = super().clean()
        honeypot = cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError('Spam detected')
        return cleaned_data

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            try:
                # Send email to you
                send_mail(
                    f'New contact from {name}',
                    f'From: {email}\n\nMessage:\n{message}',
                    'contact@haydenbussard.com',
                    ['hayden@haydenbussard.com', 'haydenbussard@outlook.com'],
                    fail_silently=False,
                )
                
                # Send automated response to the user
                send_mail(
                    'Thank You for Contacting Me!',
                    f'Dear {name},\n\nThank you for reaching out! I have received your message and will get back to you as soon as possible.\n\nBest regards,\nHayden Bussard',
                    'contact@haydenbussard.com',
                    [email],
                    fail_silently=False,
                )

                messages.success(request, 'Your message has been sent!')
                return redirect('contact')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'There was an error with your submission. Please try again.')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})