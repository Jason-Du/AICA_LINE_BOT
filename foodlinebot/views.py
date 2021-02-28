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
    var_reply_token_store = 0
    if request.method == 'GET':
        print("receive get request")
        with open('id.txt', 'r') as f:
            user_id=f.read()
        f.close()
        print(user_id)
        try:
            line_bot_api.push_message(user_id, TextSendMessage(text='message from Desktop'))
        except LineBotApiError as e:
            # error handle
            raise e
        return HttpResponse()

    elif request.method == 'POST':
        try:
            signature = request.META['HTTP_X_LINE_SIGNATURE']
            # print(request.META)

        except:
            print("NO SIGNATURE")
        body = request.body.decode('utf-8')

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

            # [{"message": {"id": "13613467708831", "text": "C", "type": "text"}, "mode": "active",
            #   "replyToken": "e01380545e5e4c788456b40c6f426bec",
            #   "source": {"type": "user", "userId": "Ubc735f7239dfd126d8816b39b11dbacb"}, "timestamp": 1614170710771,
            #   "type": "message"}]
            if event.message.text=="setreply":
                var_id = (event.source.user_id)
                with open('id.txt', 'w') as f:
                    f.write(str(var_id))
                    f.close()
            elif (event.message.text=="photo"):
                pass
                data = {
                    "name": "Jason",
                    "photo": "ON"
                }
                print(data.keys())
                # "message from desktop"
                r = requests.get('https://aaf0b0213f31.ngrok.io', params=data)
                r.close()
            elif (event.message.text == "hi"):
                pass
                data = {
                    "name": "Jason",
                    "photo": "OFF"
                }
                # print(data.keys())
                # "message from desktop"
                r = requests.get('https://aaf0b0213f31.ngrok.io/hi', params=data)
                r.close()
            else:
                pass



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
        print("ERROR")
        return HttpResponseBadRequest()