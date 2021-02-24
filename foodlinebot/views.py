from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage
import requests


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser       = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        try:
            signature = request.META['HTTP_X_LINE_SIGNATURE']
            print(signature)
        except:
            print("NO SIGNATURE")
        body = request.body.decode('utf-8')
        print(body)

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=event.message.text)
                )
            print(event.message.text)
            if (event.message.text=="photo"):
                pass
                data = {
                    "name": "Jason",
                    "photo": "ON"
                }
                print(data.keys())
                # "message from desktop"
                r = requests.get('https://11238b824f9c.ngrok.io', params=data)
                r.close()


                # try:
                #     client = paramiko.SSHClient()
                #     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #     client.connect(hostname, port, username, password)
                #     t = client.get_transport()
                #     # sftp=paramiko.SFTPClient.from_transport(t)
                #     # d = sftp.stat("/Users/allen/Dropbox/python/ssh.txt")
                #     # print (d)
                #     stdin, stdout, stderr = client.exec_command('source test.sh')
                #     # stdin, stdout, stderr = client.exec_command('ls -al')
                #     result = stdout.readlines()
                #     print(result)
                # except Exception:
                #     print('Exception!!')
                #     raise
                #
        return HttpResponse()
    else:
        return HttpResponseBadRequest()