import os

from botocore.vendored.requests.packages import urllib3


def send_message(url):
    chatbot_url = os.environ['CHATBOT_URL'] + '/sendMessage'
    fields = {
        'chat_id': os.environ['CHAT_ID'],
        'text': f"[Akaito] Server is down!\n{url}",
        'parse_mode': 'HTML'
    }

    http = urllib3.PoolManager()
    r = http.request('POST', chatbot_url, fields=fields)

    if r.status >= 400:
        exit(f"Failed to send message via telegram... ({r.status} {r.reason})")


def handle(event, context):
    url = event['Records'][0]['Sns']['MessageAttributes']['TargetUrl']['Value']
    if not url:
        exit(f"Failed to check connection... No url provided.")

    http = urllib3.PoolManager()
    r = http.request('GET', url)
    if r.status >= 300:
        send_message(url)
