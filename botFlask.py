from flask import Flask, request, json

app = Flask(__name__)

import settings
from bot import analyze


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys() or 'secret' not in data.keys():
        return 'not vk'
    if data['secret'] != settings.secret_key:
        return
    if data['type'] == 'confirmation':
        return settings.confirmation_token
    if data['type'] == 'message_new':
        data = data['object']
        user_id = data['from_id']
        msg_from_user = data['text']
        timestamp = data['date']

        #  We ignoring vk server repeated messages
        if not analyze.is_valid_timestamp(user_id, timestamp):
            return 'ok'

        points = settings.msg_to_points(msg_from_user)
        if msg_from_user == settings.btn_back or msg_from_user == settings.cmd_back:
            analyze.go_back(user_id)
        elif msg_from_user == settings.btn_restart or msg_from_user == settings.cmd_restart:
            analyze.go_to_start(user_id)
        elif points is not None:
            analyze.process(user_id, points)
        else:
            analyze.touch(user_id)

    return 'ok'
