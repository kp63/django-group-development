# askbox/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .models import Ask, Answer

# 質問一覧ページ
@login_required
def index(request):
    your_asks = Ask.objects.filter(ask_by=request.user)
    asks = Ask.objects.filter(ask_to=request.user)

    # 質問から、未回答の質問と回答済みの質問に分ける
    unreplied_asks = asks.filter(answer__isnull=True)
    replied_asks = asks.exclude(answer__isnull=True)

    return render(request, 'askbox/index.html', {
        # ログインユーザーからの質問
        'your_asks': your_asks,

        # ログインユーザー宛の質問
        'asks': asks,
        'unreplied_asks': unreplied_asks,
        'replied_asks': replied_asks,
    })

# 質問送信ページ
@login_required
def ask_question(request):
    return render(request, 'askbox/question.html')

# 質問送信ページ（ユーザー指定）
@login_required
def ask_to(request, pk):
    user = get_object_or_404(User, pk=pk)


    if request.method == 'POST':
        # 質問メッセージを取得
        question_message = request.POST.get('message')

        # 質問メッセージが空でないことを確認
        if question_message:
            # Ask モデルに質問を保存
            Ask.objects.create(
                ask_by=request.user,
                ask_to=user,
                message=question_message
            )

            messages.success(request, '質問を送信しました。')

            return redirect('askbox:index')

    return render(request, 'askbox/question_to.html', {'user': user})

# 質問返信ページ
@login_required
def reply(request, pk):
    ask = get_object_or_404(Ask, pk=pk)

    if request.method == 'POST':
        # 質問メッセージを取得
        reply_message = request.POST.get('message')

        # 質問メッセージが空でないことを確認
        if reply_message:
            # Answer モデルに回答を保存
            Answer.objects.create(
                ask=ask,
                responder=request.user,
                message=reply_message
            )

            messages.success(request, '回答を送信しました。')

            return redirect('askbox:index')

    return render(request, 'askbox/question_reply.html', {'question': ask})

# 質問一覧ページ
@login_required
def answers(request, question_id):
    question = get_object_or_404(Ask, pk=question_id)

    if request.method == 'POST':
        # 回答メッセージを取得
        answer_message = request.POST.get('answer_message')

        # 回答メッセージが空でないことを確認
        if answer_message:
            # Answer モデルに回答を保存
            Answer.objects.create(
                ask=question,
                responder=request.user,
                message=answer_message
            )
            return redirect('askbox:question_list')  # 回答後に質問一覧ページにリダイレクト

    return render(request, 'askbox/answer.html', {'question': question})
