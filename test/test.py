from ReadZif import ZifReader

zif_loc = r'C:\Main\Data\_\Baguan\Records\202001\ZD80C8F020010900QE0\ZD80C8F020010900QE0.zif'
zif_read = ZifReader(zif_loc)
patient_info = zif_read.RecordInfoGet()
patient_list = zif_read.RecordListGet()

print(patient_info.pid, patient_info.rid, patient_info.machine)
print(patient_list.loc[0, 'fid'], patient_list.loc[0, 's_t'].date())
