from django.db import models
from django.conf import settings

class Tweet(models.Model):
    #つぶやきの本文を保存
    content = models.TextField()
    #日時を保存
    created_at = models.DateTimeField(auto_now_add=True)
    #つぶやきのユーザーを参照、ユーザーを削除されたとき自動的に削除
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #画像を保存
    image = models.ImageField(upload_to='tweets', null=True, blank=True)

    def __str__(self):
        return self.content
