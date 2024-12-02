import requests
import json

from bluebird import settings

def send_teams_webhook(title: str, fields: dict):
    """
    TeamsのIncoming Webhookにアダプティブカード形式でメッセージを送信する関数
    """

    if not hasattr(settings, 'TEAMS_WEBHOOK_URL'):
        print('settings.TEAMS_WEBHOOK_URLが設定されていません。')
        return False

    webhook_url = settings.TEAMS_WEBHOOK_URL

    # フィールドをアダプティブカードのFactSet形式に変換
    facts = [{"title": key, "value": value} for key, value in fields.items()]

    print(facts)

    # ペイロードの設定
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": title,
                            "weight": "Bolder",
                            "size": "Large"
                        },
                        {
                            "type": "FactSet",
                            "facts": facts
                        }
                    ],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json"
                }
            }
        ]
    }

    # Webhookにリクエストを送信
    response = requests.post(
        webhook_url, data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        return True
    else:
        print(f'Webhook送信エラー: {response.status_code}')
        return False
