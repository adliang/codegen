import json
import os
from string import Template
from pprint import pprint

JSONFILE = 'config.json'
HEADER = '// Some comment code\n\nvoid ModBus()\n{\n\t'


os.chdir('C:\\projects\\Secheron\\codegen')
text_file = open("modbusDB.c", "w")
filetemplate = open('modbusDB.txt')
src = Template(filetemplate.read())

with open(JSONFILE) as configfile:
    data = json.load(configfile)
data = data['modBusDB']
print(json.dumps(data))
pprint(data)

reglist = list(data.keys())
print(reglist)
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
