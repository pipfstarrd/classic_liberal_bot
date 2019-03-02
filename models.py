import sqlalchemy.exc
from botFlask import db
import settings


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.SmallInteger, default=-1)
    category_index = db.Column(db.SmallInteger, default=0)

    categories = db.relationship("Category", back_populates="user")

    def __init__(self, user_id, **kwargs):
        super().__init__(id=user_id, **kwargs)

    def __repr__(self):
        return "<User(id={}, categores={}, C{}Q{})>".format(
            self.id, self.categories, self.category_index, self.position)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.SmallInteger)
    name = db.Column(db.String, nullable=False)
    points = db.Column(db.Float, default=0)
    points_history = [list(range(len(settings.quest_text[x]))) for x in range(len(settings.quest_text))]

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="categories", uselist=False)

    def __repr__(self):
        return "<Category(index={}, name='{}', points={})>".format(
            self.index, self.name, self.points)


try:
    db.session.query(User).first()
except sqlalchemy.exc.OperationalError:
    db.create_all()

