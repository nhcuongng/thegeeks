from mongoengine import *
from user import User
from answer import Answers
class Tree(Document):
    code = StringField()
    password = StringField()
    owners = ListField(ReferenceField('User'))
    point = IntField()
