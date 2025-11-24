from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import UserProfile, Project, Skill, Certification
from .serializers import (
    UserPortfolioSerializer,
    ProjectSerializer,
    SkillSerializer,
    CertificationSerializer,
    UserProfileSerializer
)

class ProjectViewSet(viewsets.ModelViewSet):
    """프로젝트 CRUD"""
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SkillViewSet(viewsets.ModelViewSet):
    """역량/스킬 CRUD"""
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CertificationViewSet(viewsets.ModelViewSet):
    """자격증 CRUD"""
    serializer_class = CertificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Certification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserPortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    """사용자 포트폴리오 조회"""
    serializer_class = UserPortfolioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """현재 로그인한 사용자의 포트폴리오"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ViewSet):
    """사용자 프로필 조회 및 수정"""
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """현재 사용자 프로필 조회"""
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def create(self, request):
        """프로필 생성 또는 수정"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
