vent_machine_info = {
    "PB840": [1, 50, ["840", "PB840", "xs840", "xsPB 840"]],
    "Maquet": [2, 50, ["Servoi", "Servos", "xsServoi", "xsServos"]],
    "Drager":
    [3, 62.5, ["V300", "Evita", "Evita4", "xsV300", "xsEvita", "xsEvita4"]],
    "SV300_SV800": [4, 50, ["SV300", "SV800", "xsSV300", "xsSV800"]],
    "V60": [5, 50, ["V60", "xsV60"]],
    "NoDefine": [7, 50, ["NoDefine"]],
    "V300": [8, 62.5, ["V300"]],
    "Vela": [11, 50, ["Vela", "xsVela"]],
    "Philips": [135, 128, ["Philips"]],
}

vent_info = {
    'PB840': {
        'NAME': ['840', 'PB840', 'xs840', 'xsPB 840'],
        'CNT_NUM': [1],
        'SAMPLE_RATE': 50,
        'VENT_TYPE': ['NIV', 'IV'],
        'VENT_MODE': ['AC', 'SIMV', 'SPONT', 'BILEVL'],
        'MAND_TYPE': ['PC', 'VC', 'VC+']
    },
    'Maquet': {
        'NAME': ['Serv', 'Servoi', 'Servos', 'xsServoi', 'xsServos'],
        'CNT_NUM': [2],
        'SAMPLE_RATE':
        50,
        'VENT_TYPE': [],
        'VENT_MODE': [
            '', ' VUN1(unused)*', 'PC', 'VC', 'PRVC', 'VS', 'SIMV_VC_PS',
            'SIMV_PC_PS', 'CPAP_PS', 'NOT_SUPP', 'SIMV_PRVC_PS', 'BIVENT',
            'PC_NIV', 'PS_CPAP_NIV', 'Nassal_opkCPAP', 'NAVA', 'VNU2*',
            'NIV_NAVA*', 'PC_NoTrigger', 'VC_NoTrigger', 'PRVC_NoTrigger',
            'VS_Mode19', 'VS_Mode20'
        ],
        'MAND_TYPE': []
    },
    'Drager': {
        'NAME': ['Evita', 'Evita4', 'V300', 'xsEvita', 'xsEvita4', 'xsV300'],
        'CNT_NUM': [3, 8],
        'SAMPLE_RATE':
        62.5,
        'VENT_TYPE': [],
        'VENT_MODE': [
            '', 'IPPV', 'IPPV/ASSIST', '', '', '', 'SIMV', 'SIMV/ASB', '', '',
            'CPAP', 'CPAP/ASB', 'MMV', 'MMV/ASB', 'BIPAP', 'SYNCHRON MASTER',
            'SYNCHRON SLAVE', 'APNEA VENTILATION', '', '', '', '', '', '', '',
            '', 'APRV', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', 'BIPAP/ASB', 'SIMV/AutoFlow', 'SIMV/ASB/AutoFlow',
            'IPPV/AutoFlow', 'IPPV/ASSIST/AutoFlow', 'MMV/AutoFlow',
            'MMV/ASB/AutoFlow', '', 'CPAP/PPS', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', 'BIPAP/ASSIST'
        ],
        'MAND_TYPE': []
    },
    'Mindray': {
        'NAME': ['SV300', 'SV800', 'xsSV300', 'xsSV800'],
        'CNT_NUM': [4],
        'SAMPLE_RATE':
        50,
        'VENT_TYPE': [],
        'VENT_MODE': [
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'STANDBY',
            'V-A/C', 'P-A/C', 'CPAP/PSV', 'V-SIMV', 'P-SIMV', 'PRVC',
            'DuoLevel', 'APRV', 'PRVC-SIMV', '', '', '', '', '', '', '',
            'O2-Therapy', '', '', 'VS', 'AMV', ''
        ],
        'MAND_TYPE': []
    },
    'v60': {
        'NAME': ['V60', 'xsV60'],
        'CNT_NUM': [5],
        'SAMPLE_RATE': 50,
        'VENT_TYPE': [],
        'VENT_MODE': ['S/T', 'PCV', 'CPAP', 'AVAPS', 'STDBY'],
        'MAND_TYPE': []
    },
    'RM_G5': {
        'NAME': ['G5'],
        'CNT_NUM': [],
        'SAMPLE_RATE':
        50,
        'VENT_TYPE': [],
        'VENT_MODE': [
            '', 'AMBIENT', '', 'SCMV', 'SIMV', 'SPONT', 'SIMV/P', 'CMV/P',
            'SIMV/APV', 'CMV/APV', 'ASV', 'DuoPAP', 'APRV', 'NIV', 'NIV/ST',
            'nCPAP/PS', 'VS', ''
        ],
        'MAND_TYPE': []
    }
}


def StringListCheck(string, list_):
    for x in list_:
        if string == x:
            return True
    return False


def ReadSamplerate(num_machine_type=None, str_machine_type=None):
    """
    num_machine_type: the machine ID from wave header
    str_machine_type: default none
    """

    if num_machine_type and type(num_machine_type) == int:

        for i in vent_machine_info.values():

            if num_machine_type == i[0]:
                refSampleRate = i[1]
                return refSampleRate

        print("1 - no matching types")

    elif str_machine_type and not num_machine_type and type(
            str_machine_type) == str:

        try:
            type_name = str_machine_type.split("-")[0]
        except:
            print("Wrong machine name")

        for i in vent_machine_info.values():

            if type_name in i[2]:
                refSampleRate = i[1]
                return refSampleRate

        print("2 - no matching types")

    else:
        print("lack of valid input")


def ReadVentMode(*args):

    machine_name = str(args[0])
    vt_num = int(args[1])
    vm_num = int(args[2])
    mt_num = int(args[3])

    vt_name = None
    mt_name = None
    vm_name = None

    machine_type = 'NaN'

    for i in list(vent_info.keys()):
        if StringListCheck(machine_name, vent_info[i]['NAME']):
            vt_name = None if not vent_info[i]['VENT_TYPE'] else vent_info[i][
                'VENT_TYPE'][vt_num]
            mt_name = None if not vent_info[i]['MAND_TYPE'] else vent_info[i][
                'MAND_TYPE'][mt_num]
            vm_name = vent_info[i]['VENT_MODE'][vm_num] if vm_num < len(
                vent_info[i]['VENT_MODE']) else str(vm_num)

    if not vm_name:
        machine_type = 'NaN'
    else:
        if not mt_name:
            machine_type = vm_name
        else:
            machine_type = vm_name + '/' + mt_name

    return machine_type