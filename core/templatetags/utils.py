from datetime import datetime
from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def datetime_for_humans(value):
    """日時オブジェクトを日本語で表示するフィルター。例: '2022年01月01日 12:34'。"""
    if not isinstance(value, datetime):
        return value

    return value.strftime("%Y年%m月%d日 %H:%M")

@register.filter
def diff_for_humans(value):
    """日時オブジェクトから経過時間を日本語で表示するフィルター。例: 'n日前' または 'n秒前'。"""
    if not isinstance(value, datetime):
        return value


    now = timezone.now()
    delta = now - value

    if delta.seconds <= 10:
        return "たった今"
    
    if delta.seconds < 60:
        return f"{delta.seconds}秒前"
    
    delta_minutes = delta.seconds // 60
    if delta_minutes < 60:
        return f"{delta_minutes}分前"
    
    delta_hours = delta_minutes // 60
    if delta_hours < 24:
        return f"{delta_hours}時間前"
    
    delta_days = delta.days
    if delta_days < 30:
        return f"{delta_days}日前"
    
    delta_months = delta_days // 30
    if delta_months < 6:
        return f"{delta_months}ヶ月前"
    
    if delta_months == 6:
        return "半年前"
    
    # 今年の場合は月日のみを表示
    if value.year == now.year:
        return value.strftime("%m月%d日")

    # それ以外は年月日を表示
    return value.strftime("%Y年%m月%d日")
