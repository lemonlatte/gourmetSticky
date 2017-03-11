#!/usr/bin/env python

from flask import Flask
from flask import abort
from flask import request
import requests
app = Flask(__name__)


BOT_TOKEN = ""
PAGE_TOKEN = ""
FB_MESSENGER_URI = "https://graph.facebook.com/v2.6/me/messages?access_token=" + PAGE_TOKEN

def send_text(reply_token, text):
    data = {
        "recipient": {"id": reply_token},
        "message": {"text": text}
    }
    r = requests.post(FB_MESSENGER_URI, json=data)
    if r.status_code != requests.codes.ok:
        print r.content
    pass

def fb_post_handler(req):
    print req.get_data()
    resp_body = req.get_json()

    for entry in resp_body["entry"]:
        for msg in entry["messaging"]:
            sender = msg['sender']['id']
            if 'postback' in msg:
                if msg['postback']['payload'] == "GET_STARTED":
                    send_text(sender, 'welcome')
            elif 'message' in msg:
                if msg['message'].get('is_echo'):
                    return ""
                text = msg['message']['text']
                send_text(sender, text)
    return ""


@app.route("/fbCallback", methods=['GET', 'POST'])
def fb_cb_handler():
    if request.method == 'POST':
        return fb_post_handler(request)
    elif request.method == 'GET':
        token = request.args.get('hub.verify_token')
        if token == BOT_TOKEN:
            return request.args.get('hub.challenge')
        else:
            abort(403)

if __name__ == "__main__":
    app.run()
