from django.http import HttpRequest #HTTPリクエストを送る #HTTPリクエストはWebブラウザからWebサーバに対しての要求や命令
from django.shortcuts import redirect, render #指定されたURLへリダイレクトを行うためのショートカット関数
#指定したテンプレートを指定したコンテキストデータと共にレンダリング（描画）して、HttpResponse を返すためのショートカット関数
from django.urls import reverse, reverse_lazy #URL名を基に、そのURLのパスを取得する関数
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic import DeleteView
from django.contrib import messages #：ユーザーに対してフラッシュメッセージを表示するためのモジュール。例えば、操作が成功した場合や失敗した場合に、その結果を通知するために使われる

from .forms import CreateVoteForm #formsモジュールから
from .models import Vote, VoteResult #modelsモジュールから

# 投票一覧を表示するビュー
class IndexView(ListView):
    template_name ='votes/index.html'
    model = Vote
    queryset = Vote.objects.all().order_by('-created_at') # 作成順にならべかえ


# 投票を新たに作成するビュー
class CreateVoteView(FormView):
    template_name = 'votes/create.html'
    form_class = CreateVoteForm
    success_url = reverse_lazy('votes:index')  #フォーム送信後のページ設定

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # ログイン中のユーザーをフォームに渡す
        return kwargs

    def form_valid(self, form):  # フォームが正しいときに実行される関数
        form.save()
        messages.success(self.request, '投票を作成しました')
        return super().form_valid(form)


# 投票フォームを表示する & 投票を受け付けるビュー
def voting(request: HttpRequest, pk: int):
    # URLで指定されたpkの投票フォームを取得
    vote = Vote.objects.get(pk=pk)

    # 投票した選択肢
    vote_result = VoteResult.objects.filter(user=request.user, vote=vote).first()
    # ユーザーと投票したユーザーが一致しているか
    # 投票した選択肢と一致しているか

    # 投票した選択肢があるとき
    if vote_result:
        is_voted = True   # 投票している
        voted_choice = vote_result.choice
    # ないとき
    else:
        is_voted = False  # 投票していない
        voted_choice = None

    # すでに投票しているときに表示させないように
    if request.method == 'POST':  # 投票されたとき
        if is_voted:  #投票している
            messages.error(request, 'すでに投票しています')
            return render(request, 'votes/form.html', {
                'object': vote,
                'choices': vote.choices.all(),
                'disabled': is_voted,
                'voted_choice': voted_choice,
            })

        # POSTされたデータから選択肢を取得
        choice_id = request.POST.get('choice')
        choice = vote.choices.get(pk=choice_id)

        if choice is None:
            # 選択肢が存在しない場合はエラーを表示
            messages.error(request, '存在しない選択肢です')
            return redirect(reverse('votes:form', kwargs={'pk': pk}))

        # VoteResultに挿入（投票結果の保存）
        VoteResult.objects.create(
            vote=vote,   # 投票先フォーム
            choice=choice,    # 選ばれた選択肢
            user=request.user # ログイン中のユーザー
        )

        return redirect(reverse('votes:completing'))

    return render(request, 'votes/form.html', {
        'object': vote,
        'choices': vote.choices.all(),
        'disabled': is_voted,
        'voted_choice': voted_choice,
    })


# 投票完了画面を表示するビュー
def completing(request: HttpRequest):
    return render(request, 'votes/complete.html')  # 投票完了画面に飛ばす

# 投票を削除するビュー
class VoteDeleteView(DeleteView):
    model=Vote
    template_name='votes/delete.html'
    success_url=reverse_lazy('votes:index')
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

# 投票結果を表示するビュー
def result(request: HttpRequest, pk: int):
    vote = Vote.objects.get(pk=pk) #pkと一致する投票を取得
    if not vote:
        messages.error(request, '存在しない投票です')
        return redirect(reverse('votes:index'))

    results = VoteResult.objects.filter(vote=vote)

    return render(request, 'votes/result.html', {
        'object': vote,
        'choices': vote.choices.all(),
        'results': results
    })
