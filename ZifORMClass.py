from peewee import *
from playhouse.sqlite_ext import JSONField

try:
    db = SqliteDatabase('tmp.db')
except:
    print('Data encoding conversion not completed !')


class RecordInfo(Model):

    rid = TextField(column_name='RecordID', primary_key=True)
    s_t = DateTimeField(column_name='StartTime')
    dev = JSONField(column_name='DeviceInfo')
    pat = JSONField(column_name='PatientInfo')
    doc = JSONField(column_name='DoctorInfo')

    class Meta():
        table_name = 'RecordInfo'
        database = db


class RecordList(Model):

    fid = TextField(column_name='FileName', primary_key=True)
    s_t = DateTimeField(column_name='StartTime')
    pat = JSONField(column_name='PatientInfo')
    doc = JSONField(column_name='DoctorInfo')

    class Meta():
        table_name = 'RecordList'
        database = db


class RecordVer(Model):

    ver = IntegerField(column_name='Version', primary_key=True)
    re1 = TextField(column_name='Reserve1')
    re2 = TextField(column_name='Reserve2')
    re3 = TextField(column_name='Reserve3')
    re4 = TextField(column_name='Reserve4')

    class Meta():
        table_name = 'RecordVer'
        database = db