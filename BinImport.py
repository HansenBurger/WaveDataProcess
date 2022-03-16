import pandas as pd
import json, sqlite3
from struct import unpack
from pathlib import Path, PurePath
from collections import defaultdict
from ZifORMClass import db, RecordInfo, RecordList


class Basic():
    def __init__(self) -> None:
        self.folder_p = r'sources/json'

    def __DataFileCheck(self, file):
        file = Path(file) if not isinstance(file, PurePath) else file
        if file.is_file():
            pass
        else:
            file = None
            print('File Not Exist !')
        return file

    def __HeadFieldsLoad(self, head_type):
        data = None
        p = Path(self.folder_p) / (head_type + '.json')
        if not p.is_file():
            print('Json File Not Exist !')
        else:
            with open(str(p)) as f:
                data = json.load(f)
        return data

    def __ReadByBytes(self, file, d_in):
        d_out = {}
        for key in d_in.keys():
            d_ = d_in[key]
            byte_l = [file.read(d_['BYTES']) for i in range(d_['SIZE'])]
            value = [unpack(d_in[key]['TYPE'], byte)[0] for byte in byte_l]
            value = value[0] if not len(value) > 1 else value
            d_out[key] = value
        return d_out

    def __DictsCombine(self, list_dicts):
        dict_ = defaultdict(list)
        for d in list_dicts:
            for k, v in d.items():
                dict_[k].append(v)
        return dict_


class WaveData(Basic):
    def __init__(self, zdt_path):
        super().__init__()
        self.__file = self._Basic__DataFileCheck(zdt_path)
        self.__head = None
        self.__resr = -1

    @property
    def resr(self):
        return self.__resr

    def __ManualSF(self):
        fields_0 = self._Basic__HeadFieldsLoad('machine_mode')
        pass

    def HeadInfoGet(self):
        fields_0 = self._Basic__HeadFieldsLoad('wave_head')
        fields_1 = self._Basic__HeadFieldsLoad('data_engine')
        with open(self.__file, 'rb') as f:
            head = self._Basic__ReadByBytes(f, fields_0)
            lod = [self._Basic__ReadByBytes(f, fields_1) for i in range(1, 33)]
            # list of dict to dict of list
            engine = self._Basic__DictsCombine(lod)
        self.__head = head
        return head, engine

    def WaveDataGet(self):
        head = self.HeadInfoGet()[0] if not self.__head else self.__head
        hsize = head['HeaderSize']
        chcnt = head['ChannelCnt']

        with open(self.__file, 'rb') as f:
            f.seek(hsize)

            pass


class ParaData(Basic):
    def __init__(self, zpx_path):
        super().__init__()
        self.__file = self._Basic__DataFileCheck(zpx_path)

    def ParaInfoGet(self):
        fields_0 = self._Basic__HeadFieldsLoad('vent_para')
        with open(self.__file, 'rb') as f:
            file_size = self.__file.stat().st_size
            para_range = int(file_size / 1024)
            lod = [
                self._Basic__ReadByBytes(f, fields_0)
                for i in range(para_range)
            ]
            para = self._Basic__DictsCombine(lod)
        return para

    def VMInter(self, machine, para_range=[]):
        pass


class RidData(Basic):
    def __init__(self, zif_path):
        super().__init__()
        self.__loc = self._Basic__DataFileCheck(zif_path)
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
            Path(self.__db).unlink()
        except:
            print('Convert DataBase not exist !')
            return

    def RecordInfoGet(self):
        self.__PreProcess()
        dict_ = {}
        src_c = RecordInfo
        q_dev = list(src_c.select())[0].dev
        q_pat = list(src_c.select())[0].pat
        dict_['icu'] = q_dev['ICU']
        dict_['machine'] = q_dev['NAME']
        dict_['age'] = q_pat['AGE']
        dict_['pid'] = q_pat['PID']
        dict_['rid'] = q_pat['RID']
        dict_['sex'] = q_pat['SEX']
        dict_['name'] = q_pat['NAME']
        dict_['remark'] = q_pat['REMARK']
        self.__DbRemove()
        return dict_

    def RecordListGet(self):
        self.__PreProcess()
        dict_ = {}
        src_c = RecordList
        query = list(src_c.select())
        dict_['fid'] = [x.fid for x in query]
        dict_['s_t'] = [x.s_t for x in query]
        self.__DbRemove()
        return dict_