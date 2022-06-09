import numpy as np
import pandas as pd
from peewee import *
import json, sqlite3
from struct import unpack
from pathlib import Path, PurePath
from collections import defaultdict
from playhouse.sqlite_ext import JSONField


class Basic():
    def __init__(self) -> None:
        self.folder_p = Path().absolute(
        ) / 'WaveDataProcess' / 'sources' / 'json'
        self.minsize = 100

    def __DataFileCheck(self, file: Path) -> Path:
        '''
        Name: DataFileCheck
        Func: Check the file prepared to be read existed or not
        Input: Path of the file to be detected (class:Path)
        Output: Result of detection (class: Path | None)
        '''
        file = Path(file) if not isinstance(file, PurePath) else file
        if file.is_file() and file.stat().st_size > self.minsize:
            pass
        else:
            file = None
            print('File not exist or not pass the validation !')
        return file

    def __HeadFieldsLoad(self, head_type: str) -> dict:
        '''
        Name: HeadFieldsLoad
        Func: Load the .json file data in specific cate
        Input: Head fileds name (class: str)
        Output: A dict about this hf's size, bytes and so (class: dict)
        '''
        data = None
        p = Path(self.folder_p) / (head_type + '.json')
        if not p.is_file():
            print('Json File Not Exist !')
        else:
            with open(str(p)) as f:
                data = json.load(f)
        return data

    def __ReadByBytes(self, file: open, d_in: dict) -> dict:
        '''
        Name: ReadByBytes(Interpretation)
        Func: Read the data information contained in the fields one by one
        Input: open file (class: open), dict contain head fields (class: dict)
        Output: head fields value in the file
        '''
        d_out = {}
        for key in d_in.keys():
            d_ = d_in[key]
            byte_l = [file.read(d_['BYTES']) for i in range(d_['SIZE'])]
            value = [unpack(d_in[key]['TYPE'], byte)[0] for byte in byte_l]
            value = value[0] if not len(value) > 1 else value
            d_out[key] = value
        return d_out

    def __DictsCombine(self, list_dicts: list) -> dict:
        '''
        Name: DictsCombine
        Func: Trans List of dict to dict of list
        Input: A list of dicts (class: list)
        Output: A dict of lists (class: dict)
        '''
        dict_ = defaultdict(list)
        for d in list_dicts:
            for k, v in d.items():
                dict_[k].append(v)
        return dict_

    def ManualSF(self, input_=None) -> int:
        '''
        Name: ManualSF
        Func: Manual read the sample rate(by num or machine_name)
        Input: Feature of the machine (class: int | str)
        Output: Sample Rate
        '''
        resr = None
        fields_0 = self._Basic__HeadFieldsLoad('machine_mode')
        if type(input_) == int:
            for vm_type in fields_0.keys():
                if input_ not in fields_0[vm_type]['CNT_NUM']:
                    pass
                else:
                    resr = fields_0[vm_type]['SAMPLE_RATE']
                    break
        elif type(input_) == str:
            input_ = input_.split('-')[0] if len(
                input_.split('-')) > 1 else input_
            for vm_type in fields_0.keys():
                if input_ not in fields_0[vm_type]['NAME']:
                    pass
                else:
                    resr = fields_0[vm_type]['SAMPLE_RATE']
                    break
        return resr


class WaveData(Basic):
    def __init__(self, zdt_path):
        super().__init__()
        self.__file = self._Basic__DataFileCheck(zdt_path)
        self.__head = None
        self.__resr = -1  # ref sample rate

    @property
    def resr(self):
        return self.__resr

    def HeadInfoGet(self) -> dict:
        if not self.__file:
            return {}, {}

        fields_0 = self._Basic__HeadFieldsLoad('wave_head')
        fields_1 = self._Basic__HeadFieldsLoad('data_engine')
        with open(self.__file, 'rb') as f:
            head = self._Basic__ReadByBytes(f, fields_0)
            lod = [self._Basic__ReadByBytes(f, fields_1) for i in range(1, 33)]
            # list of dict to dict of list
            engine = self._Basic__DictsCombine(lod)
        resr = head['RefSampleRate']
        m_cnt = head['Reserved1'][0]
        self.__head = head
        self.__resr = resr if resr > 0 and resr < 100 else self.ManualSF(m_cnt)
        return head, engine

    def WaveDataGet(self) -> dict:
        if not self.__file:
            return {}

        head = self.HeadInfoGet()[0] if not self.__head else self.__head
        hsize = head['HeaderSize']
        chcnt = head['ChannelCnt']
        d_in = []

        del head

        IndexSet = lambda x, func: [
            i for (i, val) in enumerate(x) if func(val)
        ]

        # BitInfo collection
        with open(self.__file, 'rb') as f:
            f.seek(hsize)
            byte = f.read(2)
            d_in.append(byte)
            while byte:
                byte = f.read(2)
                d_in.append(byte)
            d_in = [unpack('H', x)[0] for x in d_in[:-1]]

        if len(d_in) % chcnt != 0:
            norm_len = int(len(d_in) / chcnt) * chcnt
            d_in = d_in[:norm_len]

        d_in = np.array(d_in)

        # wave data reshape
        shape_ = (int(len(d_in) / chcnt), chcnt)
        wave_ = np.reshape((d_in - 32768) / 100, shape_).T
        del d_in

        ind, s_F, s_P, s_V = [], [], [], []

        if chcnt == 2:
            F, P, V = wave_[0], wave_[1], []
        elif chcnt in [3, 4, 5]:
            F, P, V = wave_[0], wave_[1], wave_[2]
        else:
            return {'ind': ind, 's_F': s_F, 's_P': s_P, 's_V': s_V}

        insp = False
        for i in range(len(F)):
            if F[i] == 327.67:
                insp = True
            else:
                s_F.append(F[i])
                s_P.append(P[i])
                if insp:
                    ind.append(1)
                    insp = False
                else:
                    ind.append(0)

        s_V = [0] * len(s_P)
        ind = IndexSet(ind, lambda x: x == 1)

        for i in range(len(ind) - 1):
            sumV = 0
            for j in range(ind[i], ind[i + 1]):
                sumV += (s_F[j] * 1000) / (60 * self.__resr)
                s_V[j] = sumV

        s_V = [0 if i < 0 else i for i in s_V]

        return {'ind': ind, 's_F': s_F, 's_P': s_P, 's_V': s_V}


class ParaData(Basic):
    def __init__(self, zpx_path):
        super().__init__()
        self.__file = self._Basic__DataFileCheck(zpx_path)
        self.__para = None

    def __StringCheck(self, x: str, l: list) -> bool:
        for i in l:
            if x == i:
                return True
        return False

    def ParaInfoGet(self):
        if not self.__file:
            return {}

        fields_0 = self._Basic__HeadFieldsLoad('vent_para')
        with open(self.__file, 'rb') as f:
            file_size = self.__file.stat().st_size
            para_range = int(file_size / 1024)
            lod = [
                self._Basic__ReadByBytes(f, fields_0)
                for i in range(para_range)
            ]
            para = self._Basic__DictsCombine(lod)
        self.__para = para
        return para

    def VMInter(self, m_n: str, p_sel: slice) -> list:
        if not self.__file:
            return []

        m_n = m_n.split('-')[0] if len(m_n.split('-')) > 1 else m_n
        fields_0 = self._Basic__HeadFieldsLoad('machine_mode')
        para = self.ParaInfoGet() if not self.__para else self.__para

        vm_d = {}
        vt_l = para['st_VENT_TYPE'][p_sel]
        mt_l = para['st_MAND_TYPE'][p_sel]
        vm_l = para['st_VENT_MODE'][p_sel]

        for m_t in fields_0.keys():
            if not self.__StringCheck(m_n, fields_0[m_t]['NAME']):
                continue
            else:
                vm_d = fields_0[m_t]
                vt_n_l = [] if not vm_d['VENT_TYPE'] else [
                    vm_d['VENT_TYPE'][i] for i in vt_l
                ]
                mt_n_l = [] if not vm_d['MAND_TYPE'] else [
                    vm_d['MAND_TYPE'][i] for i in mt_l
                ]
                vm_n_l = [
                    vm_d['VENT_MODE'][i]
                    if i < len(vm_d['VENT_MODE']) else str(i) for i in vm_l
                ]

        if not vm_d:
            vent_type_l = ['NaN'] * len(vm_l)
        else:
            if not mt_n_l:
                vent_type_l = vm_n_l
            else:
                vent_type_l = [
                    vm_n_l[i] + '/' + mt_n_l[i] for i in range(len(vm_n_l))
                ]

        return vent_type_l


class RidData(Basic):
    def __init__(self, zif_path: Path) -> None:
        super().__init__()
        self.__loc = self._Basic__DataFileCheck(zif_path)
        self.__db = 'tmp.db'
        self.__t_n = ['RecordInfo', 'RecordList', 'RecordVer']

    @property
    def db(self):
        return self.__db

    def __PreProcess(self):
        with sqlite3.connect(self.__loc) as con:
            try:
                con.text_factory = lambda x: x.decode('gbk')
                statements = ['SELECT * FROM ' + x for x in self.__t_n]
                df_s = [pd.read_sql(x, con) for x in statements]
            except:
                con.text_factory = lambda x: x.decode('gb18030')
                statements = ['SELECT * FROM ' + x for x in self.__t_n]
                df_s = [pd.read_sql(x, con) for x in statements]

        if not Path(self.__db).is_file():
            pass
        else:
            Path(self.__db).unlink()

        with sqlite3.connect(self.__db) as con:
            for i in range(3):
                df_s[i].to_sql(name=self.__t_n[i], con=con)

    def __DbRemove(self):
        db.close()
        # close connection to delete the database
        try:
            Path(self.__db).unlink()
        except:
            print('Convert DataBase not exist !')
            return

    def __FieldsVal(self, dict_, field):
        try:
            result_ = dict_[field]
        except:
            result_ = None
        return result_

    def RecordInfoGet(self):
        try:
            self.__PreProcess()
        except:
            return {}
        dict_ = {}
        src_c = RecordInfo
        q_dev = list(src_c.select())[0].dev
        q_pat = list(src_c.select())[0].pat
        dict_['icu'] = self.__FieldsVal(q_dev, 'ICU')
        dict_['m_n'] = self.__FieldsVal(q_dev, 'NAME')
        dict_['age'] = self.__FieldsVal(q_pat, 'AGE')
        dict_['pid'] = self.__FieldsVal(q_pat, 'PID')
        dict_['rid'] = self.__FieldsVal(q_pat, 'RID')
        dict_['sex'] = self.__FieldsVal(q_pat, 'SEX')
        dict_['name'] = self.__FieldsVal(q_pat, 'NAME')
        dict_['remark'] = self.__FieldsVal(q_pat, 'REMARK')
        self.__DbRemove()
        return dict_

    def RecordListGet(self):
        try:
            self.__PreProcess()
        except:
            return {}
        dict_ = {}
        src_c = RecordList
        query = list(src_c.select())
        dict_['fid'] = [x.fid for x in query]
        dict_['s_t'] = [x.s_t for x in query]
        self.__DbRemove()
        return dict_


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