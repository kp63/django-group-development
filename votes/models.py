from django.db import models
from django.conf import settings

# Create your models here.

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vote_forms', verbose_name='ユーザー')

    title = models.CharField(
        verbose_name='タイトル',
        max_length=100
    )

    description = models.TextField(
        verbose_name='説明',
        max_length=1000,
        blank=True,
        null=True
    )

    closed_at = models.DateTimeField(
        verbose_name='締め切り日時',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        verbose_name='作成日時',
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '投票フォーム'
        verbose_name_plural = '投票フォーム'

class Choice(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='choices', verbose_name='投票フォーム')
    value = models.CharField(verbose_name='値', max_length=100)

    def __str__(self):
        return f"{self.vote.title}の選択肢: {self.value}"

    def vote_count(self):
        return self.vote_results.count()

    class Meta:
        verbose_name = '選択肢'
        verbose_name_plural = '選択肢'

class VoteResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vote_results', verbose_name='ユーザー')
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, verbose_name='投票フォーム')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name='選択肢', related_name='vote_results')

    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)

    def __str__(self):
        return f"{self.user}は{self.choice}を選択"

    class Meta:
        verbose_name = '投票結果'
        verbose_name_plural = '投票結果'

