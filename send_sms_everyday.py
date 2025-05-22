import time
import schedule
from main import api_id, api_hash, send_sms_user
from pyrogram import Client

def send_message():
    with Client(name="my_session", api_id=api_id, api_hash=api_hash) as app:
        app.send_message(chat_id=send_sms_user, text='программа с розыгрышами все еще не сломалась :с')

schedule_time = "18:40"
schedule.every().day.at(schedule_time).do(send_message)

while True:
    schedule.run_pending()
    time.sleep(1)
