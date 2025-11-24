import sys

path = 'c:/Users/User/Desktop/HeyCoun/mvpHeycoun/mvpHeycoun/urls.py'
content = open(path, encoding='utf-8').read()

# Add imports
if 're_path' not in content:
    content = content.replace('from django.urls import path, include', 'from django.urls import path, include, re_path')

if 'import mimetypes' not in content:
    content = content.replace('from pathlib import Path', 'from pathlib import Path\nimport mimetypes\nfrom urllib.parse import unquote')

# Add serve_static function
if 'def serve_static' not in content:
    serve_static_code = '''
def serve_static(request, path):
    """정적 파일(이미지 등) 서빙"""
    path = unquote(path)  # URL 디코딩 (한글 파일명 지원)
    file_path = FRONTEND_DIR / path
    if file_path.exists() and file_path.is_file():
        content_type, _ = mimetypes.guess_type(str(file_path))
        return FileResponse(open(file_path, 'rb'), content_type=content_type or 'application/octet-stream')
    return Response({'error': 'File not found'}, status=404)
'''
    content = content.replace('    return view\n\nurlpatterns', '    return view\n' + serve_static_code + '\nurlpatterns')

# Add image serving URL pattern
if 'serve_images' not in content:
    content = content.replace(
        '    path(\'api/auth/quick/\', quick_login, name=\'quick_login\'),\n]',
        '    path(\'api/auth/quick/\', quick_login, name=\'quick_login\'),\n    # 정적 파일 서빙 (이미지 등)\n    re_path(r\'^images/(?P<path>.+)$\', serve_static, name=\'serve_images\'),\n]'
    )

open(path, 'w', encoding='utf-8').write(content)
print('URLs updated successfully')
