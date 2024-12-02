from django.db import models
from django.conf import settings

class Ask(models.Model):
    ask_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='質問者', on_delete=models.CASCADE, related_name='asked_questions', null=True, blank=True)
    ask_to = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='質問相手', on_delete=models.CASCADE, related_name='received_questions')
    message = models.TextField(verbose_name='質問内容')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    def __str__(self):
        return self.message


class Answer(models.Model):
    ask = models.OneToOneField(Ask, verbose_name='質問', on_delete=models.CASCADE, related_name='answer')  # 一対一で関連付け
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='回答者', on_delete=models.CASCADE)
    message = models.TextField(verbose_name='回答内容')
    created_at = models.DateTimeField(verbose_name='作成日', auto_now_add=True)

    def __str__(self):
        return self.message
