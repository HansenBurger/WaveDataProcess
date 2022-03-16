import BinImport
import Fundal
from pathlib import Path

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

pass