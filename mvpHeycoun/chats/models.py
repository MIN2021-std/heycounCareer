from django.db import models

class ChatMessage(models.Model):
    """채팅 메시지 저장"""
    user_message = models.TextField()      
    ai_response = models.TextField()      
    created_at = models.DateTimeField(auto_now_add=True)  
    
    class Meta:
        ordering = ['-created_at']  
        
    def __str__(self):
        return f"Chat at {self.created_at}: {self.user_message[:50]}"


class CompletedParagraph(models.Model):
    """AI가 완성한 자기소개서 문단"""
    title = models.CharField(max_length=200)             
    content = models.TextField()                          
    experience_type = models.CharField(max_length=100, blank=True)  
    summary = models.TextField(blank=True)                
    char_count = models.IntegerField(default=0)           
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)     
    
    class Meta:
        ordering = ['-created_at']  
        verbose_name = "완성된 문단"
        verbose_name_plural = "완성된 문단들"
    
    def save(self, *args, **kwargs):
        self.char_count = len(self.content)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.char_count}자)"
