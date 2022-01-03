from copy import deepcopy
import numpy as np
import re

wave_header_info = [
    ["HeaderMarker", 1, np.uint32],
    ["RTFVersion", 1, np.uint32],
    ["FileCheckCode", 1, np.uint32],
    ["HeaderSize", 1, np.uint32],
    ["Reserved1", 12, np.uint32],
    ["RecordID", 32, np.uint16],
    ["Name", 24, np.uint16],
    ["Doctor", 16, np.uint16],
    ["AddInfo", 64, np.uint16],
    ["RecordLength", 1, np.uint32],
    ["RefSampleRate", 1, np.float32],
    ["ByteLacking", 1, np.uint16],
    ["RecordType", 1, np.uint16],
    ["Reserved2", 10, np.uint32],
    ["Age", 1, np.uint32],
    ["Gender", 1, np.uint32],
    ["Height", 1, np.uint32],
    ["Weight", 1, np.uint32],
    ["AccessTime", 1, np.uint64],
    ["StartTime", 1, np.uint64],
    ["ByteLacking", 1, np.uint32],
    ["ChannelCnt", 1, np.uint32],
]

data_engine_info = [
    ["wcLabel", 64, np.int8],  # Char
    ["nSampleRate", 1, np.float32],
    ["abADCBit", 1, np.uint32],
    ["abADCRange", 1, np.uint32],
    ["nZeroValue", 1, np.uint32],
    ["enSignalType", 1, np.uint32],
    ["nColumnCnt", 1, np.uint32],
    ["dwReserve", 2, np.uint32],
]

vent_para_info = [
    # Head 64B
    ["uiMarker", 1, np.uint32],
    ["uiIndex", 1, np.uint32],
    ["uiRecTime", 1, np.uint32],
    ["uiDataIndex", 1, np.uint32],
    ["zModel", 1, np.uint16],
    ["zCode", 1, np.uint16],
    ["cDeviceID", 16, np.int8],  # Char
    ["cDocName", 16, np.int8],  # Char
    ["uiImportTime", 1, np.uint32],
    ["cReserved", 8, np.int8],  # Char
    # Parament 192B
    ["p_P_PEAK", 1, np.float32],
    ["p_P_MEAN", 1, np.float32],
    ["p_PEEP", 1, np.float32],
    ["p_IE", 1, np.float32],
    ["p_f_TOT", 1, np.float32],
    ["p_V_TI", 1, np.float32],
    ["p_V_TE", 1, np.float32],
    ["p_VE_TOT", 1, np.float32],
    ["p_O2", 1, np.float32],
    ["p_PEEP_I", 1, np.float32],
    ["p_R_DYN", 1, np.float32],
    ["p_R_STAT", 1, np.float32],
    ["p_C_DYN", 1, np.float32],
    ["p_C_STAT", 1, np.float32],
    ["p_PI_END", 1, np.float32],
    ["p_TI_SPONT", 1, np.float32],
    ["p_VE_SPONT", 1, np.float32],
    ["p_P_PL", 1, np.float32],
    ["p_EEF", 1, np.float32],
    ["p_MVi", 1, np.float32],
    ["p_NIV_Leak", 1, np.float32],
    ["p_RR_Spont", 1, np.float32],
    ["p_P_01", 1, np.float32],
    ["p_WOB_v", 1, np.float32],
    ["p_WOB_p", 1, np.float32],
    ["p_P_min", 1, np.float32],
    ["p_V_trap", 1, np.float32],
    ["p_Temp", 1, np.float32],
    ["p_VT_asb", 1, np.float32],
    ["p_Reserved", 19, np.float32],
    # Setting(NEW) 192B
    ["st_PATIENT_TYPE", 1, np.uint16],
    ["st_VENT_TYPE", 1, np.uint16],
    ["st_VENT_MODE0", 1, np.uint16],
    ["st_VENT_MODE", 1, np.uint16],
    ["st_MAND_TYPE0", 1, np.uint16],
    ["st_MAND_TYPE", 1, np.uint16],
    ["st_SPON_TYPE0", 1, np.uint16],
    ["st_SPON_TYPE", 1, np.uint16],
    ["st_f_TOT", 1, np.float32],
    ["st_O2", 1, np.float32],
    ["st_V_T", 1, np.float32],
    ["st_P_I", 1, np.float32],
    ["st_P_SUPP", 1, np.float32],
    ["st_PEEP", 1, np.float32],
    ["st_T_insp", 1, np.float32],
    ["st_T_rise", 1, np.float32],
    ["st_Tring_Type", 1, np.float32],
    ["st_V_SENS", 1, np.float32],
    ["st_P_SENS", 1, np.float32],
    ["st_V_MAX", 1, np.float32],
    ["st_T_PL", 1, np.float32],
    ["st_E_SENS", 1, np.float32],
    ["st_IBW", 1, np.float32],
    ["st_T_E", 1, np.float32],
    ["st_O2_sensor", 1, np.float32],
    ["st_IE_insp", 1, np.float32],
    ["st_IE_exp", 1, np.float32],
    ["st_P_high_d", 1, np.float32],
    ["st_T_high", 1, np.float32],
    ["st_T_low", 1, np.float32],
    ["st_P_high", 1, np.float32],
    ["st_P_low", 1, np.float32],
    ["st_T_simv", 1, np.float32],
    ["st_PEEP_i", 1, np.float32],
    ["st_F_assist", 1, np.float32],
    ["st_V_assist", 1, np.float32],
    ["st_Reserved", 16, np.float32],
    # Asphyxia
    ["apst_f_ToT", 1, np.float32],
    ["apst_VT", 1, np.float32],
    ["apst_TI", 1, np.float32],
    ["apst_PI", 1, np.float32],
    ["apst_O2", 1, np.float32],
    ["apst_F_PEAK", 1, np.float32],
    ["apst_Reserved", 10, np.float32],
    # Alarm(Trigger)
    ["ast_P_PEAK_UP", 1, np.float32],
    ["ast_P_PEAK_DOWN", 1, np.float32],
    ["ast_VE_TOT_UP", 1, np.float32],
    ["ast_VE_TOT_DOWN", 1, np.float32],
    ["ast_V_TE_MAND_UP", 1, np.float32],
    ["ast_V_TE_MAND_DOWN", 1, np.float32],
    ["ast_V_TE_SPONT_UP", 1, np.float32],
    ["ast_V_TE_SPONT_DOWN", 1, np.float32],
    ["ast_T_apnea", 1, np.float32],
    ["ast_f_TOT_UP", 1, np.float32],
    ["ast_f_TOT_DOWN", 1, np.float32],
    ["ast_V_TI_UP", 1, np.float32],
    ["ast_PEEP_UP", 1, np.float32],
    ["ast_PEEP_DOWN", 1, np.float32],
    ["ast_Reserved", 10, np.float32],
    # Alarm(Setting) 64B
    ["alarm_cnt", 1, np.int8],  # Char
    ["alarm_slience", 1, np.int8],  # Char
    ["alarm_code", 31, np.uint16],
    # BedPara 64B
    ["bed_HR", 1, np.uint16],
    ["bed_SBP", 1, np.uint16],
    ["bed_DBP", 1, np.uint16],
    ["bed_MBP", 1, np.uint16],
    ["bed_SpO2", 1, np.uint16],
    ["bed_RR", 1, np.uint16],
    ["bed_PR", 1, np.uint16],
    ["bed_CVPm", 1, np.uint16],
    ["bed_Reserved", 24, np.uint16],
    # Note 288B
    ["cNote", 128, np.int8],
    ["fReserved", 40, np.uint32],  # Char
]

record_info = {
    'pid': [1, 'PID'],
    'name': [1, 'NAME'],
    'age': [1, 'AGE'],
    'gender': [1, 'SEX'],
    'remark': [1, 'REMARK'],  # Diseases
    'dept': [1, 'DEPT'],  # Department
    'rid': [1, 'RID'],
    'machineType': [0, 'NAME'],
    'bed': [1, 'BED'],
    'time': [1, 'TIME']
}


def ImportWaveHeader(file_loc):
    """
    _Read the head info from bin file zdf_
    file_loc: the opt file location
    wave_header: return the info about zif file head
    data_engin: return the info about machine
    """

    file_loc = str(file_loc)

    # Create name list wave data dict

    wave_header_name = []
    data_engine_name = []

    for i in wave_header_info:
        wave_header_name.append(i[0])

    for i in data_engine_info:
        data_engine_name.append(i[0])

    wave_header = dict.fromkeys(wave_header_name)
    data_engine = dict.fromkeys(data_engine_name, [])

    for i in data_engine_name:
        new_list = deepcopy(data_engine[i])
        data_engine[i] = new_list

    # Open file & Read data

    file_name = file_loc.split(".")[1]

    if file_name == "zdt" or file_name == "zds":

        with open(file_loc, "rb") as fid:
            for i in range(len(wave_header_info)):
                wave_header[wave_header_info[i][0]] = np.fromfile(
                    fid, wave_header_info[i][2], wave_header_info[i][1])

            for i in range(1, 33):
                for j in range(len(data_engine_info)):
                    data_engine[data_engine_info[j][0]].append(
                        np.fromfile(fid, data_engine_info[j][2],
                                    data_engine_info[j][1]))

    return wave_header, data_engine


def ImportPara(file_loc):
    """
    _Read the parament info from zpx file_
    file_loc: the opt file location
    vent_para: main para info in vent machine
    file_size: binary file size
    """

    file_loc = str(file_loc)
    vent_para_name = []

    for i in vent_para_info:
        vent_para_name.append(i[0])

    vent_para = dict.fromkeys(vent_para_name, [])

    for i in vent_para_name:
        new_list = deepcopy(vent_para[i])
        vent_para[i] = new_list

    file_size = np.fromfile(file_loc, np.int8).size
    file_name = file_loc.split(".")[1]

    if file_name == "zps" or file_name == "zpx":
        with open(file_loc, "rb") as fid:
            for i in range(int(file_size / 1024)):
                for j in range(len(vent_para_info)):
                    vent_para[vent_para_info[j][0]].append(
                        np.fromfile(fid, vent_para_info[j][2],
                                    vent_para_info[j][1]))

    return vent_para, file_size


def ImportZif(file_loc):
    '''
    _Read the main info from zif file_
    file_loc: the opt file location
    return_dict: the info we want from zif file
    '''
    patt = r"\"(.*)\" : \"(.*)\""
    dict_num = 3
    dict_list = []
    return_dict = {}

    with open(file_loc, 'rb') as fp:

        dict_tmp = {}

        while dict_num != 0:

            try:
                line = fp.readline().decode('gbk')  # transfer to string

                if '}' in line:
                    dict_list.append(dict_tmp)
                    dict_num = dict_num - 1
                    dict_tmp = {}
                    continue

                elif '{' not in line:
                    list_ = list(re.findall(patt, line)[0])  # 0:key, 1:value
                    key = list_[0]
                    value = list_[1]

                    if not value:
                        value = None

                    dict_tmp[key] = value

            except:
                continue  # keep scaning until find the effective line

        record_name = list(record_info.keys())
        for i in record_name:
            return_dict[i] = dict_list[record_info[i][0]][record_info[i][1]]

    return return_dict
