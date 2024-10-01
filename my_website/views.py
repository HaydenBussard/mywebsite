from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django import forms

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about_me.html')

def skills(request):
    return render(request, 'skills.html')

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

def beyond_engineering(request):
    return render(request, 'beyond_engineering.html')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput())

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
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})