import vk
import vk.exceptions
import requests
import json
import settings
from threading import Timer


messages_count = {}

session = vk.Session(access_token=settings.token)
api = vk.API(session, v=5.90)


def button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


keyboard = {
    "one_time": False,
    "buttons": [
        [button(label=settings.btn_absolutely_yes, color="positive")],
        [button(label=settings.btn_probably_yes, color="positive")],
        [button(label=settings.btn_idk, color="primary")],
        [button(label=settings.btn_probably_no, color="negative")],
        [button(label=settings.btn_absolutely_no, color="negative")],
        [button(label=settings.btn_back, color="primary"),
         button(label=settings.btn_restart, color="default")]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')


def send_message(user_id, token, message, path_to_img):

    if user_id in messages_count:
        if settings.get_unixtime() - messages_count[user_id]['date'] < 660:
            messages_count[user_id]['count'] += 1
        else:
            messages_count[user_id] = {'count': 1, 'date': settings.get_unixtime()}
    else:
        messages_count[user_id] = {'count': 1, 'date': settings.get_unixtime()}

    attachment = ""
    if path_to_img != "":
        # get URL of VK server which will be used for uploading
        r = api.photos.getMessagesUploadServer(access_token=token, peer_id=int(user_id))
        # upload image to server
        r = requests.post(r['upload_url'], files={'photo': open(path_to_img, 'rb')}).json()
        # save photo from server (we need to get photo id)
        r = api.photos.saveMessagesPhoto(photo=r['photo'], server=r['server'], hash=r['hash'], access_token=token)[0]
        # compute attachment id
        attachment = 'photo{}_{}'.format(r['owner_id'], r['id'])

    try:
        if messages_count[user_id]['count'] == 98:
            send_message(user_id, token, 'Извиняюсь, флуд-контроль ВКонтакте не дает нашему боту отправлять вам такое\
            количество сообщений :(\n\n Наш бот сообщит вам, когда сможет продолжить задавать вопросы.', '')
            messages_count[user_id] = {'count': 1, 'date': settings.get_unixtime()}
            excuse = 'Извините за задержку. Работа бота восстановлена. Следующий вопрос:\n\n' + message
            Timer(660.0, send_message, [user_id, token, excuse, path_to_img]).start()
            return 'error'

        api.messages.send(access_token=token,
                          user_id=str(user_id),
                          message=message,
                          attachment=attachment,
                          keyboard=keyboard)

    except vk.exceptions.VkAPIError:
        return 'error'                                            # bot can not send >100 msg/hour to 1 user

    return 'ok'
