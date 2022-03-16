import json

test_f_p = r'sources\json\machine_mode.json'

with open(test_f_p, 'r') as f:
    data = json.load(f)

a = data.keys()

pass
