import BinImport
import seaborn as sns
from pathlib import Path
from matplotlib import pyplot as plt

data_f = Path(
    r'C:\Main\Data\_\WaveData\Extube\Records\202011\ZD883B2D20102600G3H')
f_id = 'ZD883B2D20102600G3H_212'

# zdt, zpx, zif all in the data_f

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

sns.set_style('white')
fig, (ax_p, ax_f, ax_v) = plt.subplots(3, 1, figsize=(12, 6))
ax_p.plot(P[180:620], '-', lw=5)
ax_p.set_ylabel('P', fontdict=dict(size=17), rotation=0)
ax_p.set_yticklabels([])
ax_p.set_xticklabels([])
ax_f.plot(F[180:620], '-', lw=5)
ax_f.set_ylabel('F', fontdict=dict(size=17), rotation=0)
ax_f.set_yticklabels([])
ax_f.set_xticklabels([])
ax_v.plot(V[180:620], '-', lw=5)
ax_v.set_ylabel('V', fontdict=dict(size=17), rotation=0)
ax_v.set_yticklabels([])
ax_v.set_xticklabels([])
fig.tight_layout()
sns.despine(left=True, bottom=True, right=True)

plt.show()
plt.close()
