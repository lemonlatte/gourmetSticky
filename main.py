#!/usr/bin/env python

from flask import Flask
from flask import abort
from flask import request
app = Flask(__name__)


BOT_TOKEN = ""
PAGE_TOKEN = ""


def fb_post_handler():
    return ""


@app.route("/fbCallback")
def fb_cb_handler():
    if request.method == 'POST':
        return fb_post_handler()
    elif request.method == 'GET':
        token = request.args.get('hub.verify_token')
        if token == BOT_TOKEN:
            return request.args.get('hub.challenge')
        else:
            abort(403)
    else:
        abort(400)

if __name__ == "__main__":
    app.run()
