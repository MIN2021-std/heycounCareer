from django.contrib import admin
from .models import ChatMessage, CompletedParagraph

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """관리자 페이지에서 채팅 내역 볼 수 있게"""
    list_display = ['id', 'user_message_short', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user_message', 'ai_response']
    readonly_fields = ['created_at']
    
    def user_message_short(self, obj):
        return obj.user_message[:50] + '...' if len(obj.user_message) > 50 else obj.user_message
    user_message_short.short_description = '사용자 메시지'


@admin.register(CompletedParagraph)
class CompletedParagraphAdmin(admin.ModelAdmin):
    """관리자 페이지에서 완성된 문단 관리"""
    list_display = ['id', 'title', 'char_count', 'experience_type', 'created_at']
    list_filter = ['created_at', 'experience_type']
    search_fields = ['title', 'content', 'summary']
    readonly_fields = ['char_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'experience_type')
        }),
        ('문단 내용', {
            'fields': ('content', 'char_count')
        }),
        ('대화 요약', {
            'fields': ('summary',),
            'classes': ('collapse',)  # 접을 수 있게
        }),
        ('날짜 정보', {
            'fields': ('created_at', 'updated_at')
        }),
    )
