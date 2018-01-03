from mongoengine import *

class User(Document):
    username = StringField()
    password = StringField()
    tree_id = StringField()
    code = StringField()
