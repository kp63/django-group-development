from django.urls import path
from . import views

app_name = 'votes'

urlpatterns = [
    # 投票フォーム一覧ページ
    path('', views.IndexView.as_view(), name='index'),

    # 投票フォーム作成ページ
    path('create/', views.CreateVoteView.as_view(), name='create'),

    # 投票フォーム詳細ページ & 投票ページ
    path('form/<int:pk>', views.voting, name='form'),
    # path('form/<int:pk>', views.VotingView.as_view(), name='form'),

    # 投票完了ページ
    path('vote_complete', views.completing, name='completing'),

    # 削除ページ
    path('vote/<int:pk>/delete/', views.VoteDeleteView.as_view(), name='delete'),

    # 投票結果ページ
    path('result/<int:pk>/', views.result, name='result')

]
