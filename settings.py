import os.path as os_path
import time

# Community access token for vk
token = 'group token'

# Callback API confirmation code
confirmation_token = 'group confirmation token'

# Key to confirm the sender of the data
secret_key = 'group secret key'

# ID of the VKontakte group in which the bot is running
group_id = 146469497

# Location of categoryname.txt files containing questions
path_fonts = "bot/fonts"
path_images = "bot/images"
path_question = "bot/question"

# Buttons name
btn_absolutely_yes = "Полностью согласен"
btn_probably_yes = "Скорее согласен"
btn_idk = "Не знаю | Смешанно"                      # idk = i don`t know
btn_probably_no = "Скорее не согласен"
btn_absolutely_no = "Полностью не согласен"
btn_back = "Назад"
btn_restart = "Сначала"

# Commands name
cmd_absolutely_yes = '5'
cmd_probably_yes = '4'
cmd_idk = '3'                                         # idk = i don`t know
cmd_probably_no = '2'
cmd_absolutely_no = '1'
cmd_back = '-1'
cmd_restart = '123'

# Categories
categories = {
    "economic": [True, 0, 0, "Экономика"],           # True/False - to be inversed or not to be
    "social": [False, 0, 1, "Социальная сфера"],     # 0 - number of questions in category (i will be inited below)
    "national": [True, 0, 2, "Национализм"],         # 0,1,2,...7 - id of categories, therefore map has not indexes
    "central": [False, 0, 3, "Централизация"],       # "Экономика" - name which user will see
    "revolution": [True, 0, 4, "Революционность"],
    "ecological": [False, 0, 5, "Экология"],
    "individualism": [True, 0, 6, "Индивидуализм"],
    "scientism": [False, 0, 7, "Сциентизм"]
}

# Init list of questions
quest_text = []
q = []
for name in categories.keys():
    with open(os_path.join(path_question, name + ".txt"), 'r', encoding='utf-8') as textfile:
        for line in textfile:
            q.append(line.strip())

    quest_text.append(q)
    categories[name][1] = len(q)
    q = []


# Convert user`s message to points. User can send messages with help buttons and commands
def msg_to_points(msg_from_user):
    return {
        # buttons
        btn_absolutely_yes: 1,
        btn_probably_yes: 0.7,
        btn_idk: 0,
        btn_probably_no: -0.7,
        btn_absolutely_no: -1,
        # commands
        cmd_absolutely_yes: 1,
        cmd_probably_yes: 0.7,
        cmd_idk: 0,
        cmd_probably_no: -0.7,
        cmd_absolutely_no: -1
    }.get(msg_from_user)


# Return current timestamp converted to unixtime
def get_unixtime():
    return int(time.time())
