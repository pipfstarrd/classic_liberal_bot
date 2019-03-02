from PIL import Image, ImageDraw, ImageFont
import os
import settings
import labels


class Artist:
    # constants
    _TEMPLATE_IMG_FILE = '{}/template.png'.format(settings.path_images)
    _TEMPLATE_PATH_FOR_RESULT_IMG = '{}/results_{}.png'
    _FONT_FILE_LABEL = '{}/Sports World-Regular.ttf'.format(settings.path_fonts)
    _FONT_FILE_PERCENT = '{}/KozGoPr6N-Bold.otf'.format(settings.path_fonts)
    _COLOUR_BLACK = (0, 0, 0)
    _COLOUR_WHITE = (255, 255, 255)
    _IMG_W = 1920
    _IMG_H = 1080
    _draw = None
    _user_id = None

    def __init__(self, user_id, dict_of_points):
        # create image
        self._user_id = user_id
        img = Image.new("RGB", (self._IMG_W, self._IMG_H), "black")
        self._draw = ImageDraw.Draw(img)

        # compute percents
        dict_of_results, label = self.compute_result(dict_of_points)

        # _draw 8 indicators
        for k in dict_of_results.keys():
            self.draw_one_indicator(k, dict_of_results[k])

        # unite images
        img_template = Image.open(self._TEMPLATE_IMG_FILE)
        img.paste(img_template, (0, 0), img_template)

        # _draw label
        self.draw_label(self._draw, label)

        img.save(self._TEMPLATE_PATH_FOR_RESULT_IMG.format(settings.path_images, user_id), 'png')

    def __del__(self):
        # remove file
        if self._user_id is not None:
            try:
                os.remove(self._TEMPLATE_PATH_FOR_RESULT_IMG.format(settings.path_images, self._user_id))
            except FileNotFoundError:
                print("Exception. os.remove. File not found")
            self._user_id = None

    # get path to image
    def get_path_to_img(self):
        if self._user_id is None:
            return None
        return self._TEMPLATE_PATH_FOR_RESULT_IMG.format(settings.path_images, self._user_id)

    @staticmethod
    def compute_result(dict_of_points):
        dict_of_results = {}
        label = None
        e = "economic"
        a = "social"
        n = "national"

        # compute left percent
        for k in dict_of_points.keys():
            amount_of_questions = settings.categories[k][1]
            cur_category_result = dict_of_points[k]
            dict_of_results[k] = 50 + round((50 * abs(cur_category_result)) / amount_of_questions)

            # compute left from right percent
            if settings.categories[k][0] and cur_category_result > 0:
                dict_of_results[k] = 100 - dict_of_results[k]

            # compute left from right percent
            if not settings.categories[k][0] and cur_category_result < 0:
                dict_of_results[k] = 100 - dict_of_results[k]

        # compute label
        for i in labels.labels:
            # check edges of economic category
            if (100 - dict_of_results[e]) < i[1][0] or (100 - dict_of_results[e]) > i[1][1]:
                continue

            # check edges of social category
            if dict_of_results[a] < i[2][0] or dict_of_results[a] > i[2][1]:
                continue

            # check edges of national category
            if i[3] is not None and ((100 - dict_of_results[n]) < i[3][0] or (100 - dict_of_results[n]) > i[3][1]):
                continue

            label = i[0]
            break

        return dict_of_results, label

    # call to _draw label
    def draw_label(self, _draw, label):
        # constants
        _LABEL_Y0 = 100                                                                  # handcrafted value

        # fonts & their size
        font_1st_sign = ImageFont.truetype(self._FONT_FILE_LABEL, 135)                  # only first letter!
        font_from_2nd_to_n = ImageFont.truetype(self._FONT_FILE_LABEL, 90)              # other letters
        # hack#1
        text1_w, tmp = _draw.textsize(label[0], font=font_1st_sign)                 # (it`s solution by designer)
        tmp, text1_h = _draw.textsize('Л', font=font_1st_sign)                 # (it`s solution by designer)
        # hack#2
        text2_w, tmp = _draw.textsize(label[1:], font=font_from_2nd_to_n)               # hack: get height of 2nd sign
        tmp, text2_h = _draw.textsize(label[1], font=font_from_2nd_to_n)                # and get width of all string

        # X&Y offsets for center alignment
        x_1st_sign = (self._IMG_W - (text1_w + text2_w)) / 2
        x_from_2nd_to_n = x_1st_sign + text1_w
        y_1st_sign = _LABEL_Y0
        y_from_2nd_to_n = _LABEL_Y0 + (text1_h - text2_h)

        # _draw first letter with @font_1st_sign and _draw other letters with @font_from_2nd_to_n
        _draw.text((x_1st_sign, y_1st_sign), label[0], self._COLOUR_BLACK, font=font_1st_sign)
        _draw.text((x_from_2nd_to_n, y_from_2nd_to_n), label[1:], self._COLOUR_BLACK, font=font_from_2nd_to_n)
        return

    # call to _draw one of eight indicators
    def draw_one_indicator(self, indicator_name, percent_left: int):
        # class contains information about @offsets and @color for only one of eight indicators
        class Indicator:
            RECTANGLE_H = 60                                                            # height in pixels
            TEXT_SIZE = 45
            STROKE_WIDTH = 3                                                            # width of rectangle stroke in pixels

            def __init__(self_indic, color_left, color_right, x0, y0, max_len):
                # rectangles
                self_indic.color_left = color_left
                self_indic.color_right = color_right
                self_indic.y0 = y0                                                      # top point of filling
                self_indic.y1 = y0 + self_indic.RECTANGLE_H
                self_indic.min_rec_len = 130                                            # minimal length for each indic
                self_indic.len_from_edge_to_edge = max_len                              # length of rectangle sum lengths
                self_indic.left_rec_x0 = x0                                             # left indicator edge
                self_indic.right_rec_x1 = x0 + self_indic.len_from_edge_to_edge         # right indicator edge
                                                                                        # 0% -> indic length == min_rec_len
                # texts with percents
                self_indic.font_percents = ImageFont.truetype(self._FONT_FILE_PERCENT,
                                                              self_indic.TEXT_SIZE)
                self_indic.div_left_text_x0_and_right_text_x1 = max_len - 110           # length between X0 of left text
                                                                                        # and X1 of right text
                self_indic.div_x0_and_left_text_x0 = 55
                self_indic.left_text_x0 = x0 + self_indic.div_x0_and_left_text_x0       # left edge for left percent text
                self_indic.right_text_x1 = self_indic.left_text_x0 \
                    + self_indic.div_left_text_x0_and_right_text_x1                     # right edge for right percent text

            def get_text_coordinates(self_indic, percent_right_text: str):
                _text_w, _text_h = self._draw.textsize(percent_right_text, font=self_indic.font_percents)
                _text_y0 = self_indic.y0 + (self_indic.RECTANGLE_H - _text_h) / 2
                _right_text_x0 = self_indic.right_text_x1 - _text_w                     # left edge for right percent text
                return _text_y0, _right_text_x0

            def get_lengths_of_rectangles(self_indic, right_percent):
                max_percents_px = self_indic.len_from_edge_to_edge\
                                  - (2 * self_indic.min_rec_len + self_indic.STROKE_WIDTH)
                _right_rec_len = round((max_percents_px * right_percent) / 100)
                _left_rec_len = max_percents_px - _right_rec_len
                return _left_rec_len + self_indic.min_rec_len, _right_rec_len + self_indic.min_rec_len

        _INDICATORS = {
            # left column
            "economic": Indicator(color_left=(204, 51, 51), color_right=(51, 102, 204), x0=170, y0=355, max_len=620),
            "social": Indicator(color_left=(102, 204, 153), color_right=(153, 153, 153), x0=170, y0=521, max_len=620),
            "scientism": Indicator(color_left=(102, 51, 204), color_right=(255, 153, 102), x0=170, y0=682, max_len=620),
            "revolution": Indicator(color_left=(204, 153, 102), color_right=(204, 204, 204), x0=170, y0=840, max_len=620),
            # right column
            "ecological": Indicator(color_left=(102, 102, 153), color_right=(102, 153, 51), x0=1189, y0=356, max_len=560),
            "central": Indicator(color_left=(153, 51, 153), color_right=(102, 204, 102), x0=1189, y0=521, max_len=560),
            "individualism": Indicator(color_left=(153, 51, 0), color_right=(0, 51, 153), x0=1189, y0=682, max_len=560),
            "national": Indicator(color_left=(153, 102, 102), color_right=(102, 153, 153), x0=1189, y0=848, max_len=560)
        }

        _indic = _INDICATORS[indicator_name]

        # validate extreme values
        percent_left = abs(percent_left) % 101
        percent_right = 100 - percent_left

        # rectangles & their size
        left_rec_len, right_rec_len = _indic.get_lengths_of_rectangles(percent_right)
        self._draw.rectangle([(_indic.left_rec_x0, _indic.y0), (_indic.left_rec_x0 + left_rec_len, _indic.y1)],
                             fill=_indic.color_left)
        self._draw.rectangle([(_indic.right_rec_x1 - right_rec_len, _indic.y0), (_indic.right_rec_x1, _indic.y1)],
                             fill=_indic.color_right)

        # text & their size
        text_y0, right_text_x0 = _indic.get_text_coordinates(percent_right_text="{}%".format(percent_right))
        self._draw.text((_indic.left_text_x0, text_y0), "{}%".format(percent_left), self._COLOUR_WHITE,
                        font=_indic.font_percents)
        self._draw.text((right_text_x0, text_y0), "{}%".format(percent_right), self._COLOUR_WHITE,
                        font=_indic.font_percents)
        return
