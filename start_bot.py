#!/usr/bin/python3
# импорт библиотек
import pymumble_py3
import time
import os
import shutil
import configparser
# импорт колбэков
from pymumble_py3.callbacks import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED as PCTMR
from pymumble_py3.callbacks import PYMUMBLE_CLBK_USERUPDATED as PCUU
from pymumble_py3.callbacks import PYMUMBLE_CLBK_USERCREATED as PCUC

# читаю параметры из config.ini
config = configparser.ConfigParser()
config.read('settings.ini', encoding="utf-8")
admin_list = config['Bot']['admins'].rsplit(sep=';')
# список всех пользователей
if not os.path.exists(config['Bot']['userlist']):
    f = open(config['Bot']['userlist'], 'tw', encoding='utf-8')
    f.close()
userlist = configparser.ConfigParser()
userlist.read(config['Bot']['userlist'])
# это костыль. если его не будет, бот при подключении "поздоровается" сразу со всеми, но у него не получится и он умрёт
kostyl1 = 0


# функция создаёт папки, в которых содержатся сообщения для тех, кто зашёл на канал
def create_folder_tree():
    path = config['Bot']['data_folder'] + "/"
    try:
        os.mkdir(path)
    except OSError:
        print("Создать директорию %s не удалось" % path)
    else:
        print("Успешно создана директория %s " % path)

    path2 = path + 'welcomemessage.txt'
    try:
        f = open(path2, 'tw', encoding='utf-8')
        f.close()
    except OSError:
        print("Создать файл %s не удалось" % path2)
    else:
        print("Успешно создан файл %s " % path2)
    path2 = path + 'firstwelcomemessage.txt'
    try:
        f = open(path2, 'tw', encoding='utf-8')
        f.close()
    except OSError:
        print("Создать файл %s не удалось" % path2)
    else:
        print("Успешно создан файл %s " % path2)
    for x in mumble.channels:
        # определим имя директории, которую создаём
        path3 = path + str(x) + '.' + mumble.channels[x]['name']
        try:
            os.mkdir(path3)
        except OSError:
            print("Создать директорию %s не удалось" % path3)
        else:
            print("Успешно создана директория %s " % path3)
        path4 = path + str(x) + '.' + mumble.channels[x]['name'] + '/tm_' + mumble.channels[x]['name'] + '.txt'
        try:
            f = open(path4, 'tw', encoding='utf-8')
            f.close()
        except OSError:
            print("Создать файл %s не удалось" % path4)
        else:
            print("Успешно создан файл %s " % path4)


# функция удаляет папки
def delete_folder_tree():
    path = config['Bot']['data_folder'] + "/"
    try:
        shutil.rmtree(path)
    except OSError:
        print("Удалить директорию %s не удалось" % path)
    else:
        print("Успешно удалена директория %s" % path)
    path = "bot_data/"
    try:
        os.mkdir(path)
    except OSError:
        print("Создать директорию %s не удалось" % path)
    else:
        print("Успешно создана директория %s " % path)


# функция отправляет сообщение пользователю, зашедшему на канал
def send_message_to_user(channel_id, actor):
    path = config['Bot']['data_folder'] + "/" + str(channel_id) + '.' + mumble.channels[channel_id]['name'] + '/tm_' + \
           mumble.channels[channel_id]['name'] + '.txt'
    try:
        f = open(path, 'r', encoding="utf-8")
        text = f.read()
        mumble.users[actor].send_text_message(text)
        f.close()
    except OSError:
        print('Сообщение не отправлено')
    else:
        print('Сообщение отправлено ' + mumble.users[actor]['name'] + ':' + text)


# функция отправляет сообщение пользователю, зашедшему на сервер
def welcome_message(user):
    path = config['Bot']['data_folder'] + '/welcomemessage.txt'
    try:
        f = open(path, 'r', encoding="utf-8")
        text = f.read()
        mumble.users[user['session']].send_text_message(text)
        f.close()
    except OSError:
        print('Приветствие не отправлено')
    else:
        print('Приветствие отправлено ' + mumble.users[user['session']]['name'] + ':' + text)


# функция отправляет сообщение пользователю, зашедшему на сервер впервые
def first_welcome_message(user):
    path = config['Bot']['data_folder'] + '/firstwelcomemessage.txt'
    try:
        f = open(path, 'r', encoding="utf-8")
        text = f.read()
        mumble.users[user['session']].send_text_message(text)
        f.close()
    except OSError:
        print('Приветствие не отправлено')
    else:
        print('Приветствие отправлено ' + mumble.users[user['session']]['name'] + ':' + text)


# функция проверки принадлежности пользователя к священной касте админов
def isadmin(user):
    count = 0
    i = 0
    while i < len(admin_list) - 1:
        if str(user) == str(admin_list[i]):
            count = 1
            return True
        i = i + 1
    return False


# обработчик колбэка получения сообщения от пользователя
def message_received(user):
    message_is_command = False
    if isadmin(mumble.users[user.actor]['name']) is True:
        print(mumble.users[user.actor]['name'] + " (это админ) прислал сообщение: " + user.message.strip())
    else:
        print(mumble.users[user.actor]['name'] + " прислал сообщение: " + user.message.strip())

    if user.message.strip() == "!help":
        message_is_command = True
        message = ' '
        for x in config['Command user']:
            message = message + '<p>' + config['Command user'][x] + '</p>'
        if isadmin(mumble.users[user.actor]['name']) is True:
            for x in config['Command admin']:
                message = message + '<p>' + config['Command admin'][x] + '</p>'
        mumble.users[user.actor].send_text_message(message)

    if user.message.strip() == "!createfoldertree" and isadmin(mumble.users[user.actor]['name']) == True:
        message_is_command = True
        create_folder_tree()

    if user.message.strip() == "!deletefoldertree" and isadmin(mumble.users[user.actor]['name']) == True:
        message_is_command = True
        delete_folder_tree()

    if user.message.strip() == "!users":
        message_is_command = True
        text = '<p>Список пользователей:</p>'
        x = 0
        while x < len(userlist.sections()):
            text = text + '<p>' + userlist.sections()[x] + '</p>'
            x = x + 1
        mumble.users[user.actor].send_text_message(text)

    if user.message.strip()[0:5] == "!send":
        message_is_command = True
        send_offline_message(user.actor, user.message.strip())

    if message_is_command is False:
        mumble.users[user.actor].send_text_message(user.message.strip())


# обработчик колбэка перехода пользователя по каналам
def user_change_channel(user, pos):
    if 'channel_id' in pos:  # колбэк вызывается также включением/выключением микрофона у пользователя, тут стоит фильтр "Только переходы по каналам"
        print(user['name'] + " перешел в канал " + mumble.channels[user['channel_id']]['name'])
        if user['session'] != mumble.users.myself_session:
            send_message_to_user(user['channel_id'], user['session'])


# обработчик колбэка подключения пользователя к серверу
def user_connect_server(user):
    if kostyl1 == 1:
        # дополняем список всех пользователей сервера
        if mumble.users[user['session']]['name'] in userlist:
            welcome_message(user)
            check_offline_messages(user)
        else:
            first_welcome_message(user)
            userlist.add_section(mumble.users[user['session']]['name'])
            userlist.set(mumble.users[user['session']]['name'], mumble.users[user['session']]['name'], '')
            with open(config['Bot']['userlist'], "w") as config_file:
                userlist.write(config_file)


# пользователь "проверяет" свой почтовый ящик
def check_offline_messages(user):
    for x in userlist[mumble.users[user['session']]['name']]:
        if userlist[mumble.users[user['session']]['name']][x] != '':
            text = '<p>Пользователь ' + x + ' оставил сообщение:</p>' + '<p>' + \
                   userlist[mumble.users[user['session']]['name']][x] + '</p>'
            mumble.users[user['session']].send_text_message(text)
            userlist.set(mumble.users[user['session']]['name'], x, '')
            with open(config['Bot']['userlist'], "w") as config_file:
                userlist.write(config_file)
                print('Оффлайн сообщение отправлено ' + mumble.users[user['session']]['name'] + ':' + text)


# пользователь пишет кому-то сообщение
def send_offline_message(user, command):
    command = command.rsplit(sep='!')
    error = 1
    x = 0
    # проверяю, существует ли получатель сообщения
    while x < len(userlist.sections()):
        if userlist.sections()[x] == command[2]:
            try:  # если пользователь уже отправлял ранее сообщение получателю
                userlist.set(command[2], mumble.users[user]['name'].lower(),
                             userlist[command[2]][mumble.users[user]['name']] + '<p>' + command[3] + '</p>')
            except KeyError:  # если пользователь впервые отправляет сообщение получателю
                userlist.set(command[2], mumble.users[user]['name'].lower(), '')
                userlist.set(command[2], mumble.users[user]['name'].lower(),
                             userlist[command[2]][mumble.users[user]['name']] + '<p>' + command[3] + '</p>')
            with open(config['Bot']['userlist'], "w") as config_file:
                userlist.write(config_file)
            error = 0
        x = x + 1
    if error == 1:  # если не существует получателя сообщения
        mumble.users[user].send_text_message('Какая-то ошибка, проверь формат команды или имя пользователя')
    else:
        text = 'Я передам Ваше сообщение'
        mumble.users[user].send_text_message(text)


# говорим как подключиться боту к серверу
mumble = pymumble_py3.Mumble(host=config['Server']['address'], user=config['Bot']['Bot_name'],
                             port=int(config['Server']['port']), password=config['Server']['password'],
                             certfile=config['Bot']['certfile'], reconnect=True, tokens=config['Server']['tokens'])

# к колбэкам прикручиваем функции-обработчики
mumble.callbacks.set_callback(PCTMR, message_received)
mumble.callbacks.set_callback(PCUU, user_change_channel)
mumble.callbacks.set_callback(PCUC, user_connect_server)
# подключаем бота к серверу
mumble.start()
# костыль
time.sleep(5)
print('костыль функционирует')
kostyl1 = 1
# циклим всё, чтобы бот не отключался
while 1:
    time.sleep(1)
