from django.contrib import admin
from .models import PortfolioPage, ResumeVersion, HomePage, Skill, SkillCategory, SkillsPageContent, BeyondWorkPageContent, BeyondWorkSection, SectionDetail

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
    
class SkillInline(admin.TabularInline):
    """Allows adding/editing skills directly on the SkillCategory admin page."""
    model = Skill
    extra = 1 # Number of extra forms to display
    fields = ('name', 'note', 'order',)

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'order',)
    search_fields = ('title',)
    inlines = [SkillInline]
    ordering = ('order',)

@admin.register(SkillsPageContent)
class SkillsPageContentAdmin(admin.ModelAdmin):
    # Since it's a singleton, we only want to allow editing the existing one.
    list_display = ('main_header',)
    fields = ('main_header', 'intro_text',)

    # Restrict permissions to only allow viewing/editing, not adding/deleting
    def has_add_permission(self, request):
        # Allow adding if the object doesn't exist, otherwise prevent it.
        if SkillsPageContent.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False

class SectionDetailInline(admin.TabularInline):
    """Allows adding/editing section details directly on the BeyondWorkSection admin page."""
    model = SectionDetail
    extra = 1
    fields = ('content', 'detail_type', 'order',)

@admin.register(BeyondWorkSection)
class BeyondWorkSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'intro_paragraph',)
    search_fields = ('title', 'intro_paragraph',)
    inlines = [SectionDetailInline]
    ordering = ('order',)

@admin.register(BeyondWorkPageContent)
class BeyondWorkPageContentAdmin(admin.ModelAdmin):
    list_display = ('main_header', 'browser_title',)
    fields = ('browser_title', 'main_header',)

    def has_add_permission(self, request):
        if BeyondWorkPageContent.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False