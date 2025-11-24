from rest_framework import serializers
from .models import ChatMessage, CompletedParagraph


class ChatMessageSerializer(serializers.ModelSerializer):
    """채팅 메시지 직렬화"""
    class Meta:
        model = ChatMessage
        fields = '__all__'


class CompletedParagraphSerializer(serializers.ModelSerializer):
    """완성된 문단 직렬화"""
    class Meta:
        model = CompletedParagraph
        fields = '__all__'
        read_only_fields = ['char_count', 'created_at', 'updated_at']
