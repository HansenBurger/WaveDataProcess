import BinImport
from pathlib import Path
from matplotlib import pyplot as plt

data_f = Path(r'C:\Main\Data\_\Baguan\Records\202104\ZP0EBDC521040600YAR')
f_id = 'ZP0EBDC521040600YAR_252'

zif = data_f / (f_id.split('_')[0] + '.zif')
zdt = data_f / (f_id + '.zdt')
zpx = data_f / (f_id + '.zpx')

zif_p = BinImport.RidData(zif)
zdt_p = BinImport.WaveData(zdt)
zpx_p = BinImport.ParaData(zpx)

head, _ = zdt_p.HeadInfoGet()
para = zpx_p.ParaInfoGet()
info = zif_p.RecordInfoGet()

wave = zdt_p.WaveDataGet()
F = wave['s_F']
V = wave['s_V']
P = wave['s_P']

plt.subplot(3, 1, 1)
plt.plot(P[0:500])
plt.subplot(3, 1, 2)
plt.plot(F[0:500])
plt.subplot(3, 1, 3)
plt.plot(V[0:500])
plt.show()
