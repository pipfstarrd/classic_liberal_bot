# -*- coding: utf-8 -*-
from models import User
import settings

user_list = {}


class EndOfTest(Exception):
    pass


class Survey:

    def __init__(self, user_id):
        # get corresponding user or create it
        self.user = user_list.get(user_id)
        self.newborn = False
        self.last_timestamp = -1
        self.id = user_id

        if self.user is None:
            self.newborn = True
            self.user = User()
            user_list[user_id] = self.user

    def cleanup(self):
        del user_list[self.id]

    def results(self):
        return {c: self.user.user_stats[c]['points'] for c in self.user.user_stats}

    def change_points(self, value):
        if self.user.step[1] >= 0:
            self.user.change_points(value)

    def step_question(self, backward=False):
        """Raises EndOfTest if there is no more questions"""
        question = ''
        step = -1 if backward else 1                                # step to forward or backward

        if self.user.step[1]+step == settings.categories[self.user.current_category][1]:
            if self.user.step[0] == len(settings.quest_text) - 1:
                raise EndOfTest
            else:
                self.user.next_category()

        elif self.user.step[1]+step < 0:
            if self.user.step[0] == 0:
                return 'Это первый вопрос. Назад отмотать нельзя.'
            else:
                self.user.prev_category()
        else:
            if not backward:
                self.user.next_question()
            else:
                self.user.prev_question()

        if self.user.step[1] == 0:
            # add instruction for users
            if self.user.step[0] == 0:
                question += "Для прохождения теста используйте кнопки или команды-числа:\n" \
                           "\n" \
                           "{:>3} - {}".format(settings.cmd_absolutely_yes, settings.btn_absolutely_yes) + "\n" \
                           "{:>3} - {}".format(settings.cmd_probably_yes, settings.btn_probably_yes) + "\n" \
                           "{:>3} - {}".format(settings.cmd_idk, settings.btn_idk) + "\n" \
                           "{:>3} - {}".format(settings.cmd_probably_no, settings.btn_probably_no) + "\n" \
                           "{:>3} - {}".format(settings.cmd_absolutely_no, settings.btn_absolutely_no) + "\n" \
                           "{:>3} - {}".format(settings.cmd_restart, settings.btn_restart) + "\n" \
                           "{:>3} - {}".format(settings.cmd_back, settings.btn_back) + "\n" \
                           "\n"
            # add user-friendly headers for each category (only in firsts questions)
            question += "#{}\n" \
                        "Количество вопросов: {} шт\n" \
                        "\n".format(settings.categories[self.user.current_category][3].replace(' ', '_'),
                                    settings.categories[self.user.current_category][1])

        question += settings.quest_text[self.user.step[0]][self.user.step[1]]

        return question
