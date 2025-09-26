from django.contrib import admin
from .models import PortfolioPage, ResumeVersion, HomePage

@admin.register(PortfolioPage)
class PortfolioPageAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(ResumeVersion)
class ResumeVersionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_primary')
    list_editable = ('is_primary',)

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    fieldsets = (
        ("SEO & Introduction", {
            'fields': ('title', 'headshot', 'lead_paragraph'),
        }),
        ('Professional Profile Card', {
            'fields': ('card_title_professional', 'card_text_professional'),
        }),
        ('Footer Text (Tech Stack)', {
            'fields': ('footer_text', 'website_info_link_text'),
        }),
    )
    
    # Prevent adding a second instance
    def has_add_permission(self, request):
        return not HomePage.objects.exists()