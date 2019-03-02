# -*- coding: utf-8 -*-
from bot.survey import Survey, EndOfTest, db
from messageHandler import create_answer
from Artist import Artist
from settings import get_unixtime

throttle_dict = {}


def throttle(f):
    def wrapper(*args):
        user_id = args[0]
        now = get_unixtime()
        if user_id in throttle_dict:
            if now - throttle_dict[user_id] < 660:
                return 'ok'
        f(*args)

    return wrapper


def touch(user_id, send=True):
    "Init a survey or do nothing"
    survey = Survey(user_id)
    if survey.newborn:
        return process(user_id, send=send)  # ask the first question


@throttle
def process(user_id, points=0, send=True):
    artist = None
    survey = Survey(user_id)
    survey.change_points(points)
    try:
        text = survey.step_question()                       # next question
        path_to_img = ''
    except EndOfTest:
        create_answer(user_id, "Результат обрабатывается... ждите.")
        text = ""
        artist = Artist(user_id, survey.results())          # wait 4 seconds, hard computing
        path_to_img = artist.get_path_to_img()
        survey.cleanup()

    if send:
        log = create_answer(user_id, text, path_to_img)
        if log == 'error':
            throttle_dict[user_id] = get_unixtime()
        if artist is not None:
            artist.__del__()
    return text, survey.user


@throttle
def go_back(user_id, send=True):
    survey = Survey(user_id)
    question = survey.step_question(backward=True)
    if send:
        log = create_answer(user_id, question)
        if log == 'error':
            throttle_dict[user_id] = get_unixtime()
    return question, survey.user


def go_to_start(user_id, send=True):
    survey = Survey(user_id)
    survey.user.position = -1                               # position automatically increment after step_question
    survey.user.category_index = 0                          # add we get the 1st question
    question = survey.step_question()
    if send:
        create_answer(user_id, question)
    return question, survey.user


# check timestamp of last message, and return False
# if current message is double
def is_valid_timestamp(user_id, cur_timestamp: int):
    survey = Survey(user_id)

    if survey.last_timestamp > cur_timestamp:
        return False

    survey.last_timestamp = cur_timestamp
    return True
