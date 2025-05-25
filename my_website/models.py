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