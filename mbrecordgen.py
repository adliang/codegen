#!/usr/bin/env python
# ====================================================================== #
'''
mbrecordgen.py
Reads json config file. Returns mb records json file with assigned addresses
__author__ = Andrew Liang
'''
# ====================================================================== #


import json
from shutil import copyfile
import copy
from prettytable import PrettyTable, ALL, FRAME, HEADER
from PDFWriter import PDFWriter

# Finds keys in dict_in matching key_find, returns list of corresponding values
def get_values(dict_in, key_find):

    values_list = []

    def value_gen(d):
        for key, value in d.items():
            if key == key_find:
                yield value
            elif isinstance(value, dict):
                for id_val in value_gen(value):
                    yield id_val
    for values in value_gen(dict_in):
        values_list.append(values)

    return values_list


def get_address(record_list):
    
    start_address = 5000
    used_address = []
    alloc_error = False

    # Assigns allocated addresses first
    record_list = sorted(record_list, key=lambda entry: entry['varname'])
    for entry in record_list:
        if entry.has_key('alloc'):
            alloc_address = entry['alloc']
            while any(j in list(range(alloc_address, alloc_address + entry['length'])) for j in used_address):
                alloc_address += 1
                alloc_error = True
            if alloc_error == True:
                print("%s alloc conflict. Reassigned to address %i." % (entry['varname'], alloc_address))
                alloc_error = False
            entry.update({'address': alloc_address})
            for i in list(range(0, int(entry['length']))):
                used_address.append(alloc_address + i)
        
    # Assign rest of addresses
    record_list2 = copy.copy(record_list)
    
    for entry in record_list:
        if entry.has_key('ignore'):
            record_list2.remove(entry)
        elif entry.has_key('alloc'):
            continue
        else:
            while any(j in list(range(start_address, start_address + entry['length'])) for j in used_address):
                start_address = start_address + 1
            entry.update({'address': start_address})
            for i in list(range(0, int(entry['length']))):
                used_address.append(start_address + i)
                
    record_list2 = sorted(record_list2, key=lambda entry: int(entry['address']))

    return record_list2

def pdfgen(table_data, output):
    pt = PrettyTable(["PDU", "Name", "Units", "Type", "Access", "Length"])
    pt.align = "l"
    pt.hrules = ALL
    
    for i in range(0, len(table_data)):
        pt.add_row( [
            table_data[i]['address'],
            table_data[i]['varname'],
            (table_data[i]['units'] if table_data[i].has_key('units') else ""),
            table_data[i]['type'],
            table_data[i]['access'],
            table_data[i]['length']
            ])
    lines = pt.get_string()
    pw = PDFWriter(output)
    pw.setFont('Courier', 8)
    pw.setHeader('Modbus records')
    pw.setFooter('Modbus records')
    for line in lines.split('\n'):
        pw.writeLine(line)
    pw.close()
    print('Modbus map address list PDF created (%s)' %output)




def readconfig(config_file):
# Reads config file, saves backup

    with open(config_file) as infile:
        config_data = json.load(infile)
        infile.close()

    output_file = config_file + ('-codegenbackup')
    copyfile(config_file, output_file)
    print('Config backup file created (%s)' % output_file)

    return config_data


def generate_mbmap(config_file, config_key, output_file = None):
    ''' Takes input config_file, returns json list containing entries with assigned addresses'''
    config_data = readconfig(config_file)
    mbrecords = get_values(config_data, config_key)
    parsed_records = get_address(mbrecords)
    
    # Writes address assigned records to file
    if output_file:
        with open(output_file, 'w') as outfile:
            json.dump(parsed_records, outfile, indent = 4)
            outfile.close()
            print('Modbus map address list file created (%s)' %output_file)
    with open(config_file, 'w') as outfile:
        json.dump(config_data, outfile, indent=4, sort_keys=True)
        outfile.close()
        print('%s addresses updated' % config_file)

    print('mbrecordgen.py completed')
    return parsed_records

