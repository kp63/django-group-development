from django.db.models import Count #データベース内でオブジェクトの数をカウントするために使用
from django.contrib import messages # ユーザーへの通知（エラーメッセージや成功メッセージ）を表示するために使用
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,CreateView, DeleteView, DetailView , View
from django.views.generic.edit import UpdateView
from .forms import ChatMessageForm, CreateThreadForm
from .models import Thread, ChatMessage # Thread（スレッド）とChatMessage（チャットメッセージ）のモデルをインポート
from django.urls import reverse_lazy #URLの名前を逆引きし、文字列としてURLを取得します。ビューやリダイレクト先の設定に使用
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required #ログインしていないユーザーをログインページにリダイレクトするためのデコレータ。
# Create your views here.

class IndexView(TemplateView):
    template_name = 'threads/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # スレッド一覧を取得
        threads = Thread.objects.annotate(reply_count=Count('messages'))

#スレッドを10件ずつ分割してページネーションを実装
        paginator = Paginator(threads, 10)
        page_number = self.request.GET.get('page')# 現在のページ番号を取得
        page_obj = paginator.get_page(page_number)# 該当するページのデータを取得

        context['threads'] = page_obj
        return context

# @method_decorator(login_required, name='dispatch')
#スレッド作成ページ
@method_decorator(login_required, name='dispatch')
class CreateThreadView(CreateView):
    template_name = 'threads/create_thread.html'
    form_class = CreateThreadForm
    success_url = reverse_lazy('threads:index')

    def form_valid(self, form):
        form.instance.author = self.request.user  # ログインユーザーをauthorに設定
        return super().form_valid(form)

#スレッド削除
@method_decorator(login_required, name='dispatch')
class DeleteThreadView(DeleteView):
    model = Thread
    success_url = reverse_lazy('threads:index')  # 削除後にリダイレクトするURL
    template_name = 'threads/index.html'  # 新しいページを作らずに index.html を再利用

    def get_queryset(self):
        return Thread.objects.all()

    def get(self, request, *args, **kwargs):
        # 削除に新しい画面を表示させないために、getメソッドを上書きして直接リダイレクトします。
        return self.post(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """スレッド作成者のみが削除できるように制御"""
        thread = self.get_object()
        if thread.author != request.user:
            messages.error(request, "このスレッドを削除する権限がありません。")
            return redirect('threads:index')  # インデックスページにリダイレクト
        return super().dispatch(request, *args, **kwargs)

#スレッド詳細ページ（チャット表示）
class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'threads/thread_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.get_object()

        # スレッドに関連する全メッセージを取得
        chat_messages = ChatMessage.objects.filter(thread=thread).order_by('created_at')

        # メッセージ数を取得
        message_count = chat_messages.count()

# コンテキストにデータを追加
        context['chat_messages'] = chat_messages
        context['message_count'] = message_count  # メッセージ数をコンテキストに追加
        context['form'] = ChatMessageForm()  # チャットメッセージフォーム
        return context


#チャットメッセージ投稿
@method_decorator(login_required, name='dispatch')
class CreateChatMessageView(View):
    def post(self, request, thread_id):
        thread = Thread.objects.get(id=thread_id)
        form = ChatMessageForm(request.POST)

        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.thread = thread  # チャットメッセージをスレッドに関連付け
            chat_message.author = request.user if request.user.is_authenticated else None # ユーザーが認証されていれば投稿者を設定
            chat_message.save()#メッセージを保存

        return redirect('threads:thread_detail', pk=thread_id)

# スレッド編集ビュー
@method_decorator(login_required, name='dispatch')
class EditThreadView(UpdateView):
    model = Thread
    fields = ['title']  # 編集可能なフィールド
    template_name = 'threads/edit_thread.html'

    def get_success_url(self):
        # 編集後にスレッド詳細ページへリダイレクト
        return reverse_lazy('threads:thread_detail', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        """スレッド作成者のみが編集できるように制御"""
        thread = self.get_object()  # 編集対象のスレッドを取得
        if thread.author != request.user: # 編集権限がない場合
            messages.error(request, "このスレッドを編集する権限がありません。")
            # 編集元のページを判定してリダイレクト先を切り替える
            from_page = self.request.GET.get('from')
            if from_page == 'detail':
                return redirect('threads:thread_detail', pk=thread.pk)
            else:
                return redirect('threads:index')  # インデックスページにリダイレクト
          # 権限がある場合は通常の処理を続行
        return super().dispatch(request, *args, **kwargs)


