import sqlite3
import pandas as pd
from os import remove
from data import PatientDomain
from orm import db, RecordInfo, RecordList


class BasicFunc():
    def __init__(self) -> None:
        pass


class ZifReader(BasicFunc):
    def __init__(self, zif_loc):
        super().__init__()
        self.__loc = zif_loc
        self.__db = 'tmp.db'
        self.__t_n = ['RecordInfo', 'RecordList', 'RecordVer']

    def __PreProcess(self):
        with sqlite3.connect(self.__loc) as con:
            con.text_factory = lambda x: x.decode('gbk')
            statements = ['SELECT * FROM ' + x for x in self.__t_n]
            df_s = [pd.read_sql(x, con) for x in statements]
        with sqlite3.connect(self.__db) as con:
            for i in range(3):
                df_s[i].to_sql(name=self.__t_n[i], con=con)

    def __DbRemove(self):
        db.close()  # close connection to delete the database
        try:
            remove('tmp.db')
        except:
            print('Convert DataBase not exist !')
            return

    def RecordInfoGet(self):
        self.__PreProcess()
        src_c = RecordInfo
        dst_o = PatientDomain()
        q_dev = list(src_c.select())[0].dev
        q_pat = list(src_c.select())[0].pat
        dst_o.icu = q_dev['ICU']
        dst_o.machine = q_dev['NAME']
        dst_o.age = q_pat['AGE']
        dst_o.pid = q_pat['PID']
        dst_o.rid = q_pat['RID']
        dst_o.sex = q_pat['SEX']
        dst_o.name = q_pat['NAME']
        dst_o.remark = q_pat['REMARK']
        self.__DbRemove()
        return dst_o

    def RecordListGet(self):
        self.__PreProcess()
        src_c = RecordList
        query = list(src_c.select())
        df = pd.DataFrame()
        df['fid'] = [x.fid for x in query]
        df['s_t'] = [x.s_t for x in query]
        df = df.sort_values(by='fid')
        self.__DbRemove()
        return df