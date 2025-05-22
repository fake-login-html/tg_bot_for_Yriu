import time

from pyrogram import Client, filters
from database import Db
import asyncio
import datetime
from  config import *
# import send_sms_everyday # ежедневная отправка сообщения

############################3

# async def run():

        #парсинг всех пользователей чата
        # async for m in client.get_chat_members(-1002023924728):
        #     print(m.joined_date, m.user.first_name)

        # # Получаем все сообщения из чата
        # async for message in client.get_chat_history(chat_id):
        #     print(message)

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№3

client = Client(name="my_session", api_id=api_id, api_hash=api_hash)
id_users = {} # вся инфа о юзере, оставившим коммент
send_sms_user = 6858535610

# отмечаем все посты в бд завершенными
@client.on_message(filters.command("stop"))
def update_posts(client, message):

   try:
        users_id = message.from_user.id
        date_now = datetime.datetime.now()
        if users_id in main_users:
            print(f'Розыгрыш завершен {date_now}')
            client.send_message(chat_id=send_sms_user, text='все розыгрыши остановлены')
            Db().up_posts()
   except:
       pass

@client.on_message(filters.chat(send_sms_user))
def handle_message(client, message):
    client.send_message(chat_id=send_sms_user, text='скрипт с розыгрышами еще не сломался :с')

message_id = []
# MAIN
@client.on_message(filters.chat(chat_id))
def handle_message(client, message):

    async def check_user_in_channel(app, channel, user_id):
        try:
            member = await app.get_chat_member(channel, user_id)
            member = str(member.status).split('.')[1]
            return member in ["MEMBER", "ADMINISTRATOR", "CREATOR"]
        except Exception as e:
            # print(f"Ошибка: {e}")
            return False

    def ckeck_in_group(client, channel, user_id):

        ckeck = asyncio.run(check_user_in_channel(client, channel, user_id))

        return ckeck


 ############################################

    # получаем ид сообщения
    # message_id = []
    message_id.append(message.id)


    # получаем текст сообщения
    message_text = ''
    try:
        message_text = message.text
        if message_text == None:
            message_text = message.caption
    except:
        pass

    # получаем id сообщения, для последующего ответа, по нему
    id_sms = message.id
    reply_to_message_id = message.reply_to_message_id
    date_now = datetime.datetime.now()

    # ищем все активные розырыши и сморим у них комменатрии
    try:
        posts = Db().post_use()
        for post in posts:

            id_post = post[0]
            if id_post == reply_to_message_id:

                # если написал пользователь
                if message.from_user != None:
                # получаем id
                    try:
                        id_users['id_users'] = message.from_user.id
                    except:
                        id_users['id_users'] = ''
                # получаем L_name
                    try:
                        id_users['last_name'] = message.from_user.last_name
                    except:
                        id_users['last_name'] = ''
                # получаем F_name
                    try:
                        id_users['first_name'] = message.from_user.first_name
                    except:
                        id_users['first_name'] = ''
                # получаем username
                    try:
                        id_users['username'] = f'@{message.from_user.username}'
                    except:
                        id_users['username'] = ''
                # получаем текст сообщения
                    try:
                        id_users['message_text'] = message.text
                    except:
                        id_users['message_text'] = ''

                    id_users['id_post'] = id_post
                    id_users['data_coments'] = date_now
                    users_in_post = Db().check_user_for_post(id_users)[0][0]
                    user_in_group = ckeck_in_group(client, channel, id_users['id_users'])

                    # если у конкретного поста нет пользовтеля и состоит в группе
                    if users_in_post == 0 \
                    and user_in_group == True\
                    and len(message_id) > 0:
                    # если несколько фоток, берем ид первой и чистим массив
                        test = message_id[len(message_id)-1]
                        message_id.clear()

                    # добавляем в бд пользователя
                        seral_num_user = Db().add_user(id_users)
                        print(f'Добавили в бд {id_users}')

                        # message.reply(text=f'Спасибо 🤝 Ваш номер: {seral_num_user} ✌️')
                        client.send_message(chat_id=chat_id, text=f'Спасибо 🤝 Ваш номер: {seral_num_user} ✌️', reply_to_message_id=test)#message_id[len(message_id)-1])
                        client.send_reaction(chat_id=chat_id, message_id=test, emoji="👍")

                   #если не состоит в группе
                    if user_in_group == False:
                        message.reply(text=f'💥 Чтобы участвовать в розыгрыше подпишитесь на канал 📺')

    except:
        pass

    # добавляем запись в бд, о том, что начался розыгрыш
    # если сообщение пришло из группы в чат
    try:
        if message.sender_chat.id != chat_id:
            # пересылаем сообщене, и добавляем в него порядковый номер
            if 'разыграем' in message_text:

                Db().add_post(id_sms, date_now)
                print(f'РОЗЫГРЫШ НАЧАЛСЯ!!! {date_now}')
                client.send_message(chat_id=send_sms_user, text=f'РОЗЫГРЫШ НАЧАЛСЯ!!! {date_now}')
    except:
        pass

        # print(message.reply_to_message.sender_chat.id)
    # except:
    #     pass
    ###################3
    # print(message.from_user)

    # # если написал пользователь
    # if message.from_user != None:
    # # получаем id
    #     try:
    #         id_users['id_users'] = message.from_user.id
    #     except:
    #         id_users['id_users'] = ''
    # # получаем L_name
    #     try:
    #         id_users['last_name'] = message.from_user.last_name
    #     except:
    #         id_users['last_name'] = ''
    # # получаем F_name
    #     try:
    #         id_users['first_name'] = message.from_user.first_name
    #     except:
    #         id_users['first_name'] = ''
    # # получаем username
    #     try:
    #         id_users['username'] = f'@{message.from_user.username}'
    #     except:
    #         id_users['username'] = ''





        # print(id_users)

        # try:

        # print(message.from_user)
    # print(message.from_user)


    # if message.reply_to_message:
    #     user_id = message.reply_to_message.from_user.id
    #
    #     # Получаем информацию о пользователе
    #     try:
    #         user = client.get_users(user_id)
    #         user_info = f"""
    #             ID: {user.id}
    #             Username: @{user.username if user.username else 'не указан'}
    #             First Name: {user.first_name}
    #             Last Name: {user.last_name if user.last_name else 'не указана'}
    #             Language Code: {user.language_code if user.language_code else 'не указан'}
    #             Is Bot: {user.is_bot}
    #             """
    #         print(user_info)
    #     except Exception as e:
    #         message.reply_text(f"Ошибка: {e}")

    ####################

if __name__ == "__main__":
    client.run()


