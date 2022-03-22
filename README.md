# Wave Data Process

A kit for .zdt, .zpx and .zif file reading and sort of basic processing

## Usage Requirements

1. python version: 3.7+

2. package require:
    1. pandas: latest
    2. peewee: latest

## File Structure

Main file structure

```shell
.
├── BinImport.py
├── README.md
├── _test.py
└── sources
    └── json
        ├── data_engine.json
        ├── machine_mode.json
        ├── vent_para.json
        └── wave_head.json
```

Description:

1. BinImport.py: Kit core code file

2. _test.py: Function test

3. README.md: Read me now! (tp-tp)

4. source: Dir to save the static source file

## How To Use

First of all, import the BinImport

```python
from WaveDataProcess import BinImport
```

### Zif Read

Example Code

```python
zif_loc = 'folder/XXXX.zif'
process = BinImport.RidData(zif_loc)
p_info = process.RecordInfoGet()
p_list = process.RecordListGet()
```

**p_info**: contain the RID basic info

**p_list**: contain each Records' recording time and recording info(hour by hour)

Return feilds can be enlarge on requirment

### Zdt Read

Example Code

```python
zdt_loc = 'folder/XXXX.zdt'
process = BinImport.WaveData(zdt_loc)
head, _ = process.HeadInfoGet()
wave = process.WaveDataGet()
F, P, V = wave['s_F'], wave['s_P'], wave['s_V']
```

**head**: contain .zdt head info (mainly about RefSampleRate)

F, P, V: describe the three dimensions of breathing data

p_ind: the start point of each breath

### Zpx Read

Example Code

```python
zpx_loc = 'folder/XXXX.zpx'
process = BinImport.ParaData(zpx_loc)
para = process.ParaInfoGet()
vm_l = process.VMInter('machine_name', slice(0,100,1))
```

para: a dict of list contain vent machine's para data in each sampling time

vm_l: return the vent mode of specific slice
