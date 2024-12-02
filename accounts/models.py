import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField('メールアドレス', unique=True)
    def get_avatar(self, size: int = 38):
        # md5でハッシュ化したメールアドレスを使ってGravatarのURLを生成
        md5 = hashlib.md5(self.email.encode()).hexdigest()
        if size:
            return f'https://www.gravatar.com/avatar/{md5}?d=retro&s={size}'
        else:
            return f'https://www.gravatar.com/avatar/{md5}?d=retro'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='profile')
    bio = models.TextField(verbose_name='自己紹介', null=True, blank=True)
    birth_date = models.DateField(verbose_name='生年月日', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'プロフィール'
        verbose_name_plural = 'プロフィール'
