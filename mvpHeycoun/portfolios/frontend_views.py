from django.http import FileResponse
from django.views.static import serve
from django.conf import settings
from pathlib import Path
import os

# 프론트엔드 파일 경로
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / 'front-end'

def serve_frontend_file(request, filename):
    """프론트엔드 파일 서빙"""
    file_path = FRONTEND_DIR / filename
    
    if file_path.exists() and file_path.is_file():
        return FileResponse(open(file_path, 'rb'), content_type='text/html')
    
    # 없으면 index 역할을 하는 login 페이지로
    if filename == '':
        login_file = FRONTEND_DIR / 'login_api.html'
        return FileResponse(open(login_file, 'rb'), content_type='text/html')
    
    return FileResponse(status=404)
