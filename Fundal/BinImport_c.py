from copy import deepcopy
import numpy as np

wave_header_info = {
    "HeaderMarker": [np.uint32, 1],
    "RTFVersion": [np.uint32, 1],
    "FileCheckCode": [np.uint32, 1],
    "HeaderSize": [np.uint32, 1],
    "Reserved1": [np.uint32, 12],
    "RecordID": [np.uint16, 32],
    "Name": [np.uint16, 24],
    "Doctor": [np.uint16, 16],
    "AddInfo": [np.uint16, 64],
    "RecordLength": [np.uint32, 1],
    "RefSampleRate": [np.float32, 1],
    "ByteLacking": [np.uint16, 1],
    "RecordType": [np.uint16, 1],
    "Reserved2": [np.uint32, 10],
    "Age": [np.uint32, 1],
    "Gender": [np.uint32, 1],
    "Height": [np.uint32, 1],
    "Weight": [np.uint32, 1],
    "AccessTime": [np.uint64, 1],
    "StartTime": [np.uint64, 1],
    "ByteLacking": [np.uint32, 1],
    "ChannelCnt": [np.uint32, 1],
}

data_engine_info = {
    "wcLabel": [np.int8, 64],  # Char
    "nSampleRate": [np.float32, 1],
    "abADCBit": [np.uint32, 1],
    "abADCRange": [np.uint32, 1],
    "nZeroValue": [np.uint32, 1],
    "enSignalType": [np.uint32, 1],
    "nColumnCnt": [np.uint32, 1],
    "dwReserve": [np.uint32, 2],
}

vent_para_info = {
    # Head 64B
    "uiMarker": [np.uint32, 1],
    "uiIndex": [np.uint32, 1],
    "uiRecTime": [np.uint32, 1],
    "uiDataIndex": [np.uint32, 1],
    "zModel": [np.uint16, 1],
    "zCode": [np.uint16, 1],
    "cDeviceID": [np.int8, 16],  # Char
    "cDocName": [np.int8, 16],  # Char
    "uiImportTime": [np.uint32, 1],
    "cReserved": [np.int8, 8],  # Char
    # Parament 192B
    "p_P_PEAK": [np.float32, 1],
    "p_P_MEAN": [np.float32, 1],
    "p_PEEP": [np.float32, 1],
    "p_IE": [np.float32, 1],
    "p_f_TOT": [np.float32, 1],
    "p_V_TI": [np.float32, 1],
    "p_V_TE": [np.float32, 1],
    "p_VE_TOT": [np.float32, 1],
    "p_O2": [np.float32, 1],
    "p_PEEP_I": [np.float32, 1],
    "p_R_DYN": [np.float32, 1],
    "p_R_STAT": [np.float32, 1],
    "p_C_DYN": [np.float32, 1],
    "p_C_STAT": [np.float32, 1],
    "p_PI_END": [np.float32, 1],
    "p_TI_SPONT": [np.float32, 1],
    "p_VE_SPONT": [np.float32, 1],
    "p_P_PL": [np.float32, 1],
    "p_EEF": [np.float32, 1],
    "p_MVi": [np.float32, 1],
    "p_NIV_Leak": [np.float32, 1],
    "p_RR_Spont": [np.float32, 1],
    "p_P_01": [np.float32, 1],
    "p_WOB_v": [np.float32, 1],
    "p_WOB_p": [np.float32, 1],
    "p_P_min": [np.float32, 1],
    "p_V_trap": [np.float32, 1],
    "p_Temp": [np.float32, 1],
    "p_VT_asb": [np.float32, 1],
    "p_Reserved": [np.float32, 19],
    # Setting(NEW) 192B
    "st_PATIENT_TYPE": [np.uint16, 1],
    "st_VENT_TYPE": [np.uint16, 1],
    "st_VENT_MODE0": [np.uint16, 1],
    "st_VENT_MODE": [np.uint16, 1],
    "st_MAND_TYPE0": [np.uint16, 1],
    "st_MAND_TYPE": [np.uint16, 1],
    "st_SPON_TYPE0": [np.uint16, 1],
    "st_SPON_TYPE": [np.uint16, 1],
    "st_f_TOT": [np.float32, 1],
    "st_O2": [np.float32, 1],
    "st_V_T": [np.float32, 1],
    "st_P_I": [np.float32, 1],
    "st_P_SUPP": [np.float32, 1],
    "st_PEEP": [np.float32, 1],
    "st_T_insp": [np.float32, 1],
    "st_T_rise": [np.float32, 1],
    "st_Tring_Type": [np.float32, 1],
    "st_V_SENS": [np.float32, 1],
    "st_P_SENS": [np.float32, 1],
    "st_V_MAX": [np.float32, 1],
    "st_T_PL": [np.float32, 1],
    "st_E_SENS": [np.float32, 1],
    "st_IBW": [np.float32, 1],
    "st_T_E": [np.float32, 1],
    "st_O2_sensor": [np.float32, 1],
    "st_IE_insp": [np.float32, 1],
    "st_IE_exp": [np.float32, 1],
    "st_P_high_d": [np.float32, 1],
    "st_T_high": [np.float32, 1],
    "st_T_low": [np.float32, 1],
    "st_P_high": [np.float32, 1],
    "st_P_low": [np.float32, 1],
    "st_T_simv": [np.float32, 1],
    "st_PEEP_i": [np.float32, 1],
    "st_F_assist": [np.float32, 1],
    "st_V_assist": [np.float32, 1],
    "st_Reserved": [np.float32, 16],
    # Asphyxia
    "apst_f_ToT": [np.float32, 1],
    "apst_VT": [np.float32, 1],
    "apst_TI": [np.float32, 1],
    "apst_PI": [np.float32, 1],
    "apst_O2": [np.float32, 1],
    "apst_F_PEAK": [np.float32, 1],
    "apst_Reserved": [np.float32, 16],
    # Alarm(Trigger)
    "ast_P_PEAK_UP": [np.float32, 1],
    "ast_P_PEAK_DOWN": [np.float32, 1],
    "ast_VE_TOT_UP": [np.float32, 1],
    "ast_VE_TOT_DOWN": [np.float32, 1],
    "ast_V_TE_MAND_UP": [np.float32, 1],
    "ast_V_TE_MAND_DOWN": [np.float32, 1],
    "ast_V_TE_SPONT_UP": [np.float32, 1],
    "ast_V_TE_SPONT_DOWN": [np.float32, 1],
    "ast_T_apnea": [np.float32, 1],
    "ast_f_TOT_UP": [np.float32, 1],
    "ast_f_TOT_DOWN": [np.float32, 1],
    "ast_V_TI_UP": [np.float32, 1],
    "ast_PEEP_UP": [np.float32, 1],
    "ast_PEEP_DOWN": [np.float32, 1],
    "ast_Reserved": [np.float32, 10],
    # Alarm(Setting) 64B
    "alarm_cnt": [np.int8, 1],  # Char
    "alarm_slience": [np.int8, 1],  # Char
    "alarm_code": [np.uint16, 31],
    # BedPara 64B
    "bed_HR": [np.uint16, 1],
    "bed_SBP": [np.uint16, 1],
    "bed_DBP": [np.uint16, 1],
    "bed_MBP": [np.uint16, 1],
    "bed_SpO2": [np.uint16, 1],
    "bed_RR": [np.uint16, 1],
    "bed_PR": [np.uint16, 1],
    "bed_CVPm": [np.uint16, 1],
    "bed_Reserved": [np.uint16, 24],
    # Note 288B
    "cNote": [np.int8, 128],
    "fReserved": [np.uint32, 40],  # Char
}


def ImportWaveHeader(file_loc):
    """
    _Read the head info from bin file zdf_
    file_loc: the opt file location
    wave_header: return the info about zif file head
    data_engin: return the info about machine
    """

    # Create name list wave data dict

    wave_header_name = wave_header_info.keys()
    data_engine_name = data_engine_info.keys()

    wave_header = dict.fromkeys(wave_header_name)
    data_engine = dict.fromkeys(data_engine_name, [])

    for i in data_engine_name:
        new_list = deepcopy(data_engine[i])
        data_engine[i] = new_list

    # Open file & Read data

    file_name = file_loc.split(".")[1]

    if file_name == "zdt" or file_name == "zds":

        with open(file_loc, "rb") as fid:
            for i in wave_header_name:
                wave_header[i] = np.fromfile(fid, wave_header_info[i][0],
                                             wave_header_info[i][1])

            for i in range(32):
                for j in data_engine_name:
                    data_engine[j].append(
                        np.fromfile(fid, data_engine_info[j][0],
                                    data_engine_info[j][1]))

    return wave_header, data_engine


def ImportPara(file_loc):
    """
    _Read the parament info from zpx file_
    file_loc: the opt file location
    vent_para: main para info in vent machine
    file_size: binary file size
    """

    vent_para_name = vent_para_info.keys()
    vent_para = dict.fromkeys(vent_para_name, [])

    for i in vent_para_name:
        new_list = deepcopy(vent_para[i])
        vent_para[i] = new_list

    file_size = np.fromfile(file_loc, np.int8).size
    file_name = file_loc.split(".")[1]

    if file_name == "zps" or file_name == "zpx":
        with open(file_loc, "rb") as fid:
            for i in range(int(file_size / 1024)):
                for j in vent_para_name:
                    vent_para[j].append(
                        np.fromfile(fid, vent_para_info[j][0],
                                    vent_para_info[j][1]))

    return vent_para, file_size
