from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tweets'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('delete/<int:pk>/', views.DeleteTweetView.as_view(), name='delete_tweet'),
    path('tweets/', views.CreateTweetView.as_view(), name='create'),
    path('tweet_results/',views.TweetResultsView.as_view(), name='results')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

