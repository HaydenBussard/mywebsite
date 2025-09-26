import os
from django.db import models
from django.core.exceptions import ValidationError

def validate_resume_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed: .pdf, .doc, .docx')

class PortfolioPage(models.Model):
    title = models.CharField(max_length=200)
    intro_text = models.TextField(blank=True, help_text="Intro or lead paragraph")
    at_a_glance = models.TextField(blank=True, help_text="Short summary or 'At a Glance' section")
    headshot = models.ImageField(upload_to='headshots/', blank=True, null=True)
    my_resume_header = models.TextField(blank=True, help_text="word choice for Resume Section header")

    def __str__(self):
        return self.title
    
class HomePage(models.Model):
    """Model to manage the content of the main home page (home.html)."""
    
    # SEO/Browser Title
    title = models.CharField(
        max_length=100, 
        default="Hayden Bussard",
        help_text="The title that appears in the browser tab."
    )
    
    # Headshot Image
    headshot = models.ImageField(
        upload_to='headshots/', 
        blank=True, 
        null=True,
        help_text="The main circular profile photo displayed on the home page."
    )
    
    # Lead Paragraph
    lead_paragraph = models.CharField(
        max_length=255, 
        default="Welcome to my personal website!",
        help_text="The main welcoming sentence under the headshot."
    )
    
    # Professional Profile Card Fields
    card_title_professional = models.CharField(
        max_length=100, 
        default="Professional Profile",
        help_text="Title for the primary call-to-action card."
    )
    card_text_professional = models.TextField(
        default="Learn about my background and explore my professional experiences.",
        help_text="Text content inside the primary call-to-action card."
    )
    
    # Footer/SEO Text
    footer_text = models.TextField(
        help_text="The small paragraph at the bottom describing the tech stack.",
        default="This website was developed using Django (a Python web framework), Bootstrap for responsive design, and it's hosted on Heroku, allowing for easy scaling and management."
    )
    website_info_link_text = models.CharField(
        max_length=255,
        default="To learn more about how this site was built, click here.",
        help_text="The entire text for the small link below the footer text. Use '$$$' where the link should go."
    )

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"

    def __str__(self):
        return "Home Page Global Content" 

    # Logic to ensure only one instance can be saved
    def save(self, *args, **kwargs):
        if not self.pk and HomePage.objects.exists():
            # Only raise validation error if a new instance is being created and one already exists
            raise ValidationError('Only one HomePage instance is allowed.')
        super().save(*args, **kwargs)

class ResumeVersion(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='resumes/',
        validators=[validate_resume_file_extension],
        help_text="Upload a PDF or Word document (.pdf, .doc, .docx)"
    )
    description = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def file_extension(self):
        return os.path.splitext(self.file.name)[1][1:].upper()  # e.g., 'PDF', 'DOCX'