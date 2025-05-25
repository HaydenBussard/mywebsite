from django.contrib import admin
from .models import PortfolioPage, ResumeVersion

@admin.register(PortfolioPage)
class PortfolioPageAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(ResumeVersion)
class ResumeVersionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_primary')
    list_editable = ('is_primary',)