from mongoengine import *

class Answers(Document):
    username = StringField()
    question = StringField()
    answer1 = StringField()
    answer2 = StringField()
    answer3 = StringField()
    answer4 = StringField()
    right_answer = StringField()
    tree_id = StringField()
