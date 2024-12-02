from django.urls import path
from .views import IndexView, CreateThreadView, DeleteThreadView, ThreadDetailView, CreateChatMessageView, EditThreadView
from .import views

app_name = 'threads'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', CreateThreadView.as_view(), name='create_thread'),
    path('<int:pk>/delete/', DeleteThreadView.as_view(), name='delete_thread'),
    path('thread/<int:pk>/edit/', views.EditThreadView.as_view(), name='edit_thread'),  # 編集ページ用URL
    path('<int:pk>/', ThreadDetailView.as_view(), name='thread_detail'),# スレッド詳細ページ（チャット表示）
    path('<int:thread_id>/message/', CreateChatMessageView.as_view(), name='create_chat_message'),  # チャットメッセージ送信

    # Add more URL patterns here
]
