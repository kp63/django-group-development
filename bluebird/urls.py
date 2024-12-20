"""
URL configuration for bluebird project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ #各々チームのメンバーが担当した場所
    path('admin/', admin.site.urls),
    path('threads/', include('threads.urls')),
    path('tweet/', include('tweets.urls')),
    path('vote/', include('votes.urls')),
    path('askbox/', include('askbox.urls')),
    path('contact/', include('contact.urls')),
    path('', include('accounts.urls')),
    path('', include('core.urls')), #基本ページ
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #アップロードされた画像の置き場
