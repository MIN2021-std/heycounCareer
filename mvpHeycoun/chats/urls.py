from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'chats'

# REST API 라우터
router = DefaultRouter()
router.register(r'paragraphs', views.CompletedParagraphViewSet, basename='paragraph')

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('api/message/', views.api_message, name='api_message'),
    path('api/', include(router.urls)),  # /chats/api/paragraphs/
]