from mongoengine import *
from user import User
from answer import Answers
class Tree(Document):
    code = StringField()
    password = StringField()
    owners = ListField(ReferenceField('User'))
    answers = ListField(ReferenceField('Answers'))
    point = IntField()
