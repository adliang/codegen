#!/usr/bin/env python
# ====================================================================== #
'''
mbrecordgen.py
Reads json config file. Returns mb records json file with assigned addresses
__author__ = Andrew Liang
'''
# ====================================================================== #

# TODO rewrite as class

import json
from shutil import copyfile


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
    record_list = sorted(record_list, key=lambda entry: entry['varname'])
    alloc_error = False

    # Assigns allocated addresses first
    for entry in record_list:
        try:
            if entry['alloc']:
                alloc_address = entry['alloc']
                while any(j in list(range(alloc_address, alloc_address+entry['length'])) for j in used_address):
                    alloc_address += 1
                    alloc_error = True
                if alloc_error == True:
                    print("%s alloc conflict. Reassigned to address %i." % (entry['varname'], alloc_address))
                    alloc_error = False
                entry.update({'address': alloc_address})
                for i in list(range(0, int(entry['length']))):
                    used_address.append(alloc_address + i)
        except KeyError:
            continue

    # Assign rest of addresses
    for entry in record_list:
        try:
            if entry['alloc']:
                continue
        except KeyError:
            while any(j in list(range(start_address, start_address + entry['length'])) for j in used_address):
                start_address = start_address + 1
            entry.update({'address': start_address})
            for i in list(range(0, int(entry['length']))):
                used_address.append(start_address + i)
    record_list = sorted(record_list, key=lambda entry: int(entry['address']))

    return record_list

# ---------------------------------------------------------------------- #
# Reads config file, saves backup
def readconfig(config_file):


    with open(config_file) as infile:
        config_data = json.load(infile)
        infile.close()

    output_file = config_file + ('.backup')
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

# DELETE - Debugging
if __name__ == "__main__":
    generate_mbmap(config_file = 'config.json', output_file = 'mbrecords.json', config_key = 'mbrecord')
#