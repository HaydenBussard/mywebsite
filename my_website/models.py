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
    
class SkillCategory(models.Model):
    """
    Represents a category of skills (e.g., 'Technical Skills', 'Soft Skills').
    """
    title = models.CharField(max_length=100, unique=True, help_text="The title for this skills section (e.g., Technical Skills, Soft Skills).")
    order = models.IntegerField(default=0, help_text="The order in which categories should appear on the page (lower number means earlier).")

    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class Skill(models.Model):
    """
    Represents an individual skill item under a category.
    """
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills',
        help_text="The category this skill belongs to."
    )
    name = models.CharField(max_length=255, help_text="The text for the skill item (e.g., Technical Problem Solving).")
    # Optional: You can add an extra field for a note/clarification like you had for Portuguese
    note = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Optional note/clarification for the skill (e.g., I have not renewed that certificate)."
    )
    order = models.IntegerField(default=0, help_text="The order in which skills should appear within their category.")

    class Meta:
        verbose_name = "Skill Item"
        verbose_name_plural = "Skill Items"
        ordering = ['order', 'name']
        unique_together = ('category', 'name') # Ensures no duplicate skill names within the same category

    def __str__(self):
        return f"{self.name} ({self.category.title})"

from django.db import models

# ... (SkillCategory and Skill models remain the same)

class SkillsPageContent(models.Model):
    """
    A singleton model to hold the customizable content for the Skills page.
    """
    # MODIFIED: Added blank=True and null=True
    main_header = models.CharField(
        max_length=200,
        default="My Skills",
        blank=True, # Allows the field to be empty in the Admin form
        null=True,  # Allows the database to store NULL if the field is empty
        help_text="The main heading for the page (e.g., 'My Skills', 'Skillset Breakdown'). Leave blank to display no main header."
    )
    # ... (intro_text and the rest of the model remain the same)
    intro_text = models.TextField(
        blank=True,
        null=True,
        help_text="Optional introductory text for the skills page."
    )

    class Meta:
        verbose_name = "Skills Page Content (Singleton)"
        verbose_name_plural = "Skills Page Content (Singleton)"

    def __str__(self):
        return "Skills Page Content"

    # Enforce the singleton pattern
    def save(self, *args, **kwargs):
        self.pk = 1
        super(SkillsPageContent, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass # Prevent deletion

class BeyondWorkPageContent(models.Model):
    """
    A singleton model to hold the customizable content for the Beyond Work page.
    """
    main_header = models.CharField(
        max_length=200,
        default="Beyond Work: Who I Am",
        blank=True,
        null=True,
        help_text="The main H1 heading for the page. Leave blank to display no main header."
    )
    
    # The title for the browser tab
    browser_title = models.CharField(
        max_length=100,
        default="Beyond Work",
        help_text="The title that appears in the browser tab."
    )

    class Meta:
        verbose_name = "Beyond Work Page Content (Singleton)"
        verbose_name_plural = "Beyond Work Page Content (Singleton)"

    def __str__(self):
        return "Beyond Work Page Content"

    # Enforce the singleton pattern
    def save(self, *args, **kwargs):
        self.pk = 1
        super(BeyondWorkPageContent, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass # Prevent deletion

# --- New Models for Dynamic Sections and Lists ---

class BeyondWorkSection(models.Model):
    """
    Represents a major content section (the H2 headings) on the page.
    """
    title = models.CharField(
        max_length=100,
        help_text="The heading for this section (e.g., 'Lifelong Learner', 'Very Active')."
    )
    intro_paragraph = models.TextField(
        blank=True,
        null=True,
        help_text="The main paragraph text that appears immediately under the section title."
    )
    order = models.IntegerField(
        default=0,
        help_text="The order in which sections should appear (lower number means earlier)."
    )

    class Meta:
        verbose_name = "Beyond Work Section"
        verbose_name_plural = "Beyond Work Sections"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class SectionDetail(models.Model):
    """
    Represents individual content details: either a list item or an extra paragraph.
    """
    DETAIL_TYPE_CHOICES = [
        ('LI', 'List Item (Bullet Point)'),
        ('P', 'Paragraph'),
    ]

    section = models.ForeignKey(
        BeyondWorkSection,
        on_delete=models.CASCADE,
        related_name='details',
        help_text="The section this detail belongs to."
    )
    content = models.TextField(
        help_text="The text content for this detail."
    )
    detail_type = models.CharField(
        max_length=2,
        choices=DETAIL_TYPE_CHOICES,
        default='LI',
        help_text="Select 'List Item' for a bullet point, or 'Paragraph' for extra text."
    )
    order = models.IntegerField(
        default=0,
        help_text="The order in which details should appear within their section."
    )

    class Meta:
        verbose_name = "Section Detail"
        verbose_name_plural = "Section Details"
        ordering = ['order']

    def __str__(self):
        return f"[{self.detail_type}] {self.content[:50]}..."
