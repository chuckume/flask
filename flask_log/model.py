import datetime
from peewee import *
from flask_login import UserMixin

db = SqliteDatabase('test.db')

class Trader(Model):
    name = CharField(unique=True)
    account = CharField()
    password = CharField()
    created_at = TimestampField(utc=True)

    class Meta:
        database = db
        indexes = (
            # create a unique constraint
            (('name', 'account'), True),
        )

def create_tables():
    db.connect()
    db.create_tables([Trader], safe=True)
    db.close()

create_tables()

# Generate testing data if DB empty
a=Trader.select()
try:
	a[0]
except IndexError:
	Trader.create(name='user1', account='account1', password='abcxyz')
	Trader.create(name='user2', account='account2', password='abcxyz')

class User(UserMixin):
    def __init__(self, id, active=True):
          self.id = id
          self.active = active
