et paste
i#!/usr/bin/env python

import json
import requests
import time
import urllib

#from dbhelper import DBHelper
#db = DBHelper()

#def handle_updates(updates):
#    for update in updates["result"]:
#        try:
#            text = update["message"]["text"]
#               chat = update["message"]["chat"]["id"]
#            items = db.get_items()
#            if text in items:
#                db.delete_item(text)
#                items = db.get_items()
#            else:
#                db.add_item(text)
#                items = db.get_items()
#            message = "\n".join(items)
#            send_message(message, chat)
#        except KeyError:
#            pass


TOKEN = "239825803:AAHd0ynYPYdYWnrXHS-2Q9-oSUEt4yPfxGk"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


#def get_updates():
#    url = URL + "getUpdates"
#    js = get_json_from_url(url)
#    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    message = updates["result"][last_update]["message"]
    if 'text' in message:
        type = 'text'
        message_id = updates["result"][last_update]["message"]["message_id"]
        content = updates["result"][last_update]["message"]["text"]
    if 'photo' in message:
        type = 'photo'
        message_id = updates["result"][last_update]["message"]["message_id"]
        content = updates["result"][last_update]["message"]["photo"][0]["file_id"]

    chat_id = message["chat"]["id"]
    return (message_id, type, content, chat_id)

''' /sendPhoto" -F chat_id="-1001354803703" -F photo="@/home/makky/Pictures/497909859.jpeg" -F caption="*max*" -F parse_mode="Markdown" '''

def send_photo(content, chat_id, reply_markup=None):
    content = urllib.parse.quote_plus(content)
    url = URL + "/sendPhoto?photo={}&chat_id={}".format(content, chat_id)
    url_channel = URL + "sendPhoto?photo={}&chat_id=-1001354803703".format(content)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)
    get_url(url_channel)

def send_message(content, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(content)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    url_channel = URL + "sendMessage?text={}&chat_id=-1001354803703".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)
    get_url(url_channel)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def handle_updates(updates):
    for update in updates["result"]:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        items = db.get_items()
        if text == "/done":
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        elif text in items:
            db.delete_item(text)
            items = db.get_items()
            keyboard = build_keyboard(items)
            send_message("Select an item to delete", chat, keyboard)
        else:
            db.add_item(text)
            items = db.get_items()
            message = "\n".join(items)
            send_message(message, chat)


def main():
#     db.setup()
    last_textchat = (None, None)
    last_message_id = None
    while True:
        message_id, type, content, chat_id = get_last_chat_id_and_text(get_updates())
#        print(message_id, type, content, chat_id)
        if message_id != last_message_id:
            if type == 'text':
                send_message(content, chat_id)
                last_message_id = message_id
            if type == 'photo':
                send_photo(content, chat_id)
                last_message_id = message_id

        time.sleep(0.5)


if __name__ == '__main__':
    main()

