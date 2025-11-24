from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Project, Skill, Certification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'profile_image', 'created_at', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'year', 'month', 'category', 'parts', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'proficiency', 'created_at']
        read_only_fields = ['created_at']

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'title', 'issuer', 'issue_date', 'expiry_date', 'credential_id', 'credential_url', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class UserPortfolioSerializer(serializers.ModelSerializer):
    """사용자의 전체 포트폴리오"""
    projects = ProjectSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'projects', 'skills', 'certifications']
