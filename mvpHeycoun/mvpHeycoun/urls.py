"""
URL configuration for mvpHeycoun project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import FileResponse, Http404
from rest_framework.routers import DefaultRouter
from portfolios.views import (
    ProjectViewSet,
    SkillViewSet,
    CertificationViewSet,
    UserPortfolioViewSet,
    UserProfileViewSet
)
from portfolios.auth_views import login, signup, logout, quick_login
from rest_framework.response import Response
from rest_framework.decorators import api_view
from pathlib import Path
import mimetypes
from urllib.parse import unquote

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'certifications', CertificationViewSet, basename='certification')
router.register(r'portfolios', UserPortfolioViewSet, basename='portfolio')
router.register(r'profile', UserProfileViewSet, basename='profile')

FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / 'front-end'

@api_view(['GET'])
def api_root(request):
    return Response({
        'message': 'HEYCOUN API',
        'version': '1.0',
        'endpoints': {
            'auth': '/api/auth/',
            'projects': '/api/projects/',
            'skills': '/api/skills/',
            'certifications': '/api/certifications/',
            'portfolio': '/api/portfolios/',
        }
    })

def serve_html(filename):
    def view(request):
        file_path = FRONTEND_DIR / filename
        if file_path.exists():
            return FileResponse(open(file_path, 'rb'), content_type='text/html; charset=utf-8')
        raise Http404('File not found')
    return view

def serve_static(request, path):
    """정적 파일(이미지 등) 서빙"""
    decoded_path = unquote(path)  # URL 디코딩 (한글 파일명 지원)
    file_path = FRONTEND_DIR / 'images' / decoded_path
    if file_path.exists() and file_path.is_file():
        content_type, _ = mimetypes.guess_type(str(file_path))
        return FileResponse(open(file_path, 'rb'), content_type=content_type or 'application/octet-stream')
    raise Http404('File not found')

urlpatterns = [
    path('', serve_html('intro.html'), name='intro'),
    path('intro/', serve_html('intro.html'), name='intro_page'),
    path('home/', serve_html('home.html'), name='home'),
    path('login/', serve_html('login_api.html'), name='login_page'),
    path('signup/', serve_html('signup.html'), name='signup_page'),
    path('portfolio/', serve_html('portfolio.html'), name='portfolio_page'),
    path('paragraphs/', serve_html('paragraphs.html'), name='paragraphs_page'),
    path('guide/', serve_html('guide.html'), name='guide_page'),
    path('project_explain.html', serve_html('project_explain.html'), name='project_explain'),
    path('team_explain.html', serve_html('team_explain.html'), name='team_explain'),
    path('admin/', admin.site.urls),
    path('chats/', include('chats.urls')),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/login/', login, name='login'),
    path('api/auth/signup/', signup, name='signup'),
    path('api/auth/logout/', logout, name='logout'),
    path('api/auth/quick/', quick_login, name='quick_login'),
    # 정적 파일 서빙 (이미지 등)
    re_path(r'^images/(?P<path>.+)$', serve_static, name='serve_images'),
]
