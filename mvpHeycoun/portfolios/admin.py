from django.contrib import admin
from .models import UserProfile, Project, Skill, Certification

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__username']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'category', 'year', 'month']
    list_filter = ['category', 'year']
    search_fields = ['user__username', 'title']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'proficiency']
    list_filter = ['proficiency']
    search_fields = ['user__username', 'name']

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'issuer', 'issue_date']
    list_filter = ['issue_date']
    search_fields = ['user__username', 'title', 'issuer']
