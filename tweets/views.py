from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView, DeleteView
from .models import Tweet
from .forms import TweetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class IndexView(ListView):
    model=Tweet
    template_name = 'tweets/index.html'
    context_object_name = 'tweets'
    #ランダムですべてのつぶやきを取得
    def get_queryset(self):
        return Tweet.objects.all().order_by('?')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


@method_decorator(login_required, name='dispatch')
class MypageView(ListView,LoginRequiredMixin):
    model = Tweet
    template_name = 'tweets/mypage.html'
    context_object_name = 'tweets'
    #ログインしているユーザーのつぶやきを降順に表示
    def get_queryset(self):
        return Tweet.objects.filter(user=self.request.user).order_by('-created_at')

class CreateTweetView(CreateView):
    model = Tweet
    form_class = TweetForm
    template_name = 'tweets/mypage.html'
    success_url = reverse_lazy('tweets:mypage')

    #フォームが無効の時エラーを出す
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response

    #フォームの保存
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteTweetView(DeleteView):
    model = Tweet
    template_name = 'tweets/tweet_delete.html'
    success_url = reverse_lazy('tweets:mypage')

class TweetResultsView(ListView):
    model = Tweet
    template_name = 'tweets/tweet_results.html'
    context_object_name = 'results'
    success_url = reverse_lazy('tweets:results')
    #検索結果を表示する
    def get_queryset(self):
        #検索ワードを取得
        query = self.request.GET.get('q')
        if query:#一致した文字列、ユーザー名を取得
            return Tweet.objects.filter(
                Q(content__icontains=query) | Q(user__username__icontains=query)
            ).order_by('-created_at')#降順に並べ替え
        return Tweet.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
