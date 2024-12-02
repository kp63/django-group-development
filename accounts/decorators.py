from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def guest_required(view_func):
    """
    ログインしている場合は指定されたURLにリダイレクトするデコレーター
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')  # ログイン済みユーザーはトップページへリダイレクト
        return view_func(request, *args, **kwargs)
    return wrapper
