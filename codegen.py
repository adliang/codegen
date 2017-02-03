import json
import os
import string
from string import Template
from pprint import pprint

JSONFILE = 'config.json'
COIL_ADDRESS = 0000
DISCIN_ADDRESS = 1000
INREG_ADDRESS = 3000
HOLDREG_ADDRESS = 4000

os.chdir('C:\\users\\Andrew\\Documents\\ELMG\\codegen')
text_file = open("modbusDB.c", "w")
filetemplate = open('modbusDB.txt')
src = Template(filetemplate.read())
mbObjects = {"coil": [], "discIn" : [], "inReg" : [], "holdReg" : []}
rawfileread = src.safe_substitute()
print(rawfileread)

with open(JSONFILE) as configfile:
    data = json.load(configfile)
record_list = data['Table']['Settings']['Versions']['mbrecords']
pprint(record_list)
# Finds all dict values under the key mbrecords. Does not work as intended; multiple 'branches' of mbrecords in config tree
'''
record_list = []
def id_generator(d):
    for k, v in d.items():
        if k == "mbrecords":
            yield v
        elif isinstance(v, dict):
            for id_val in id_generator(v):
                yield id_val

for _ in id_generator(data):
    record_list.append(_)'''

# Sort through each mbrecord element by type
for recIndex in range(0, len(record_list)):
    recEntry = record_list[recIndex]
    if recEntry['type'] == 'BIN':
        if recEntry['access'] == 'RW':
            mbObjects['coil'].append(recIndex)
            address = COIL_ADDRESS
            COIL_ADDRESS = COIL_ADDRESS + 1
        elif recEntry['access'] == 'RO':
            mbObjects['discIn'].append(recIndex)
            address = DISCIN_ADDRESS
            DISCIN_ADDRESS = DISCIN_ADDRESS + 1
    else:
        if recEntry['access'] == 'RO':
            mbObjects['inReg'].append(recIndex)
            address = INREG_ADDRESS
            if recEntry['type'][-2:] == '32':
                INREG_ADDRESS = INREG_ADDRESS + 2
            else:
                INREG_ADDRESS = INREG_ADDRESS + 1
        elif recEntry['access'] == 'RW':
            mbObjects['holdReg'].append(recIndex)
            address = HOLDREG_ADDRESS
            if recEntry['type'][-2:] == '32':
                HOLDREG_ADDRESS = HOLDREG_ADDRESS + 2
            else:
                HOLDREG_ADDRESS = HOLDREG_ADDRESS + 1
    d = {'address': address, 'name': recEntry['name'], 'type' : recEntry['type']}

    result = src.substitute(d)
    text_file.write(result)
    print(result)

pprint(mbObjects)

text_file.close()
'''
reglist = list(data.keys())
print(reglist)
HEADER = '// Some comment code\n\nvoid ModBus()\n{\n\t'
text_file.write(HEADER)

for regindex in range(0, len(reglist)):
    addrlist = (data[reglist[regindex]])

    for i in range(0,len(addrlist)):
        d = { 'address':(int(reglist[regindex]) + i), 'name':addrlist[i]['name'], 'type':addrlist[i]['type'] }

        result = src.substitute(d)
        text_file.write(result)
        print(result)

filetemplate.close()
text_file.write('}')

text_file.close()
'''