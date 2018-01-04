from mongoengine import *
# import mlab
class Image(Document):
    image = StringField()
# mlab.connect()
# new_image = Image('http://farm7.static.flickr.com/6215/6286018298_b6af252e8c_o.jpg')
# new_image.save()
