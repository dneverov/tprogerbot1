#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
# /var/www/test/tprogerbot/my_env/tprogerbot1/tprogerbot_class.py
# Run: python3 tprogerbot_class.py
#
# Килька @bot_xpeHobot

# git clone https://github.com/dneverov/tprogerbot1

import os
import requests  
import datetime

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            #last_update = get_result[len(get_result)]
            last_update = None

        return last_update


#
bot_token = os.environ["BOT_TPROGERBOT_TOKEN"]
greet_bot = BotHandler(bot_token)  
greetings = ('здравствуй', 'привет', 'ку', 'здорово', 'hi', 'hello', 'how are you')  
now = datetime.datetime.now()

def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        # Addedfrom comments to the article
        if isinstance(last_update, list):
        	last_update_id = last_update[-1]['update_id']
        elif last_update == None:
        	continue
        else:
        	last_update_id = last_update['update_id']


        ## last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        
        has_greetings = last_chat_text.lower() in greetings

        if has_greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, '1 Доброе утро, {}'.format(last_chat_name))
            #today += 1

        elif has_greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, '2 Добрый день, {}'.format(last_chat_name))
            #today += 1

        elif has_greetings and today == now.day and 17 <= hour <= 23:
            greet_bot.send_message(last_chat_id, '3 Добрый вечер, {}'.format(last_chat_name))
            #today += 1

        elif has_greetings and today == now.day and 0 <= hour < 6:
            greet_bot.send_message(last_chat_id, '4 Доброй ночи, {}'.format(last_chat_name))
            #today += 1

        else:
        	greet_bot.send_message(last_chat_id, '0 Что-то пошло не так, {}!'.format(last_chat_name))

        new_offset = last_update_id + 1


if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()