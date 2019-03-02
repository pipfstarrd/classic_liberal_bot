import logging
from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
db = SQLAlchemy(app)

import settings
from bot import analyze


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return settings.confirmation_token
    if data['type'] == 'message_new':
        data = data['object']
        user_id = data['from_id']
        msg_from_user = data['text']
        timestamp = data['date']

        logging.basicConfig(filename='bot/logs/logfile.txt', level=logging.INFO)
        werkzeug = logging.getLogger('werkzeug')
        werkzeug.setLevel(logging.ERROR)


        # we ignoring vk server repeated messages
        if not analyze.is_valid_timestamp(user_id, timestamp):
            return 'ok'

        points = settings.msg_to_points(msg_from_user)
        if msg_from_user == settings.btn_back or msg_from_user == settings.cmd_back:
            analyze.go_back(user_id)
        elif msg_from_user == settings.btn_restart or msg_from_user == settings.cmd_restart:
            analyze.go_to_start(user_id)
        elif points is not None:
            logging.info('Пользователь {} ответил на вопрос, заданный модулем survay: "{}"'\
                         .format(user_id, msg_from_user))
            analyze.process(user_id, points)
        else:
            analyze.touch(user_id)

    return 'ok'
