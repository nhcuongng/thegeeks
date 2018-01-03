import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds137957.mlab.com:37957/thegeeks

host = "ds137957.mlab.com"
port = 37957
db_name = "thegeeks"
user_name = "admin"
password = "admin"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())
