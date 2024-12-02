from django.db import models
from django.conf import settings

# スレッドモデル
class Thread(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # 自動的に更新日時を記録するフィールド

    def __str__(self):
        return self.title

    def message_count(self):
        # メッセージ数をカウント（リプライも含める）
        return self.messages.count()

# チャットメッセージモデル
class ChatMessage(models.Model):
    message = models.TextField(max_length=255)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
