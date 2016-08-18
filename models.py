import time
import uuid

from orm import Model, StringField, BooleanField, FloatField, IntegerField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time)


class ZhitiaoItem(Model):
    __table__ = 'zhitiaoitem'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    keywords = StringField(ddl='varchar(500)')
    distance = IntegerField()
    num = IntegerField()
    lng = FloatField()
    lat = FloatField()
    alt = FloatField()
    owner = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)
