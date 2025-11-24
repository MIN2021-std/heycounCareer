from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import UserProfile

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """사용자 로그인"""
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        })
    else:
        return Response(
            {'error': '인증 실패'},
            status=status.HTTP_401_UNAUTHORIZED
        )

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """사용자 회원가입"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    first_name = request.data.get('first_name', '')

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': '이미 존재하는 사용자명입니다'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name
    )

    # 프로필 자동 생성
    UserProfile.objects.create(user=user)

    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'email': user.email
    }, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
def logout(request):
    """로그아웃"""
    try:
        request.user.auth_token.delete()
    except:
        pass
    return Response({'message': '로그아웃되었습니다'})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def quick_login(request):
    """회원가입 없이 아이디로 바로 토큰 발급(없으면 자동 생성)"""
    username = request.data.get('username')
    password = request.data.get('password', '')

    if not username:
        return Response({'error': 'username이 필요합니다'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(username=username, defaults={'email': '', 'first_name': ''})

    if created:
        # 비밀번호가 있으면 저장, 없으면 사용 불가 비밀번호 설정
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        # 프로필 자동 생성
        UserProfile.objects.create(user=user)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'email': user.email
    })
