from django.urls import path
from . import views

app_name = 'askbox'

urlpatterns = [
    # トップページ
    path('', views.index, name='index'),

    # 質問送信ページ
    path('send/', views.ask_question, name='ask_question'),
    path('send/<int:pk>/', views.ask_to, name='ask_to'),

    # 質問返信ページ
    path('reply/<int:pk>/', views.reply, name='reply'),

    # 質問一覧ページ
    path('questions/', views.answers, name='answer'),

]
