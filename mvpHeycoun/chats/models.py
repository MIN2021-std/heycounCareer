from django.db import models

class ChatMessage(models.Model):
    """채팅 메시지 저장"""
    user_message = models.TextField()      # 사용자가 입력한 메시지
    ai_response = models.TextField()       # AI가 응답한 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    
    class Meta:
        ordering = ['-created_at']  # 최신순 정렬
        
    def __str__(self):
        return f"Chat at {self.created_at}: {self.user_message[:50]}"


class CompletedParagraph(models.Model):
    """AI가 완성한 자기소개서 문단"""
    title = models.CharField(max_length=200)              # 제목 (예: "백다방 2년")
    content = models.TextField()                          # AI가 만든 문단 내용
    experience_type = models.CharField(max_length=100, blank=True)  # 경험 종류 (프로젝트, 인턴십 등)
    summary = models.TextField(blank=True)                # 대화 요약
    char_count = models.IntegerField(default=0)           # 글자 수
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)      # 수정 날짜
    
    class Meta:
        ordering = ['-created_at']  # 최신순 정렬
        verbose_name = "완성된 문단"
        verbose_name_plural = "완성된 문단들"
    
    def save(self, *args, **kwargs):
        # 자동으로 글자 수 계산
        self.char_count = len(self.content)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.char_count}자)"
