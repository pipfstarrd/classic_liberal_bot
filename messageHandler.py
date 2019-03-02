import vkapi
import settings


def create_answer(user_id, message, path_to_img=""):
    return vkapi.send_message(user_id, settings.token, message[0:-1], path_to_img)

