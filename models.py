import settings


class User:

    def __init__(self):
        # First number of self.step is the category number, the second number is the question number in this category
        self.step = [0, -1]
        self.user_stats = {name: {'points': 0, 'answers': [0 for i in range(settings.categories[name][1])]}
                           for name in settings.categories.keys()}
        self.categories = [cat for cat in settings.categories.keys()]
        self.current_category = self.categories[0]

    def next_question(self):
        self.step[1] += 1

    def prev_question(self):
        self.change_points(0)
        self.step[1] -= 1

    def change_points(self, points):
        self.user_stats[self.current_category]['answers'][self.step[1]] = points
        self.user_stats[self.current_category]['points'] = sum(self.user_stats[self.current_category]['answers'])

    def next_category(self):
        self.step = [self.step[0] + 1, 0]
        self.current_category = self.categories[self.step[0]]

    def prev_category(self):
        self.current_category = self.categories[self.step[0] - 1]
        self.step = [self.step[0] - 1, settings.categories[self.current_category][1] - 1]
