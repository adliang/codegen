'''Reads json config file. Returns mb records json file with assigned addresses'''
import json
from pprint import pprint

CONFIGFILE = 'config.json'

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
        for entry in values:
            values_list.append(entry)

    return values_list

# Assigns addresses to Modbus table. Returns list of of assigned Modbus addresses
def assign_mbaddress(record_list):

    mb_table = {"coil": {}, "discIn": {}, "inReg": {}, "holdReg": {}}
    mb_list = []
    for record in record_list:
        # Get word length
        if record['type'][-2:] == '32':
            record['length'] = 2
        else:
            record['length'] = 1

        # Get table location, set initial address location
        if record['type'] == 'BIT':
            if record['access'] == 'RW':
                table_type = 'coil'
                address = '0'
            elif record['access'] == 'RO':
                table_type = 'discIn'
                address = '1000'
        else:
            if record['access'] == 'RO':
                table_type = 'inReg'
                address = '3000'
            elif record['access'] == 'RW':
                table_type = 'holdReg'
                address = '4000'

        # Get next available table address
        if mb_table[table_type]:
            prev_addr = max(mb_table[table_type], key=int)
            address = str(int(prev_addr) + mb_table[table_type][prev_addr]['length'])

        record['address'] = address
        mb_table[table_type][address] = record
        mb_list.append(record)
        pprint(record)

    pprint(mb_table)
    pprint(mb_list)

    return mb_table



def main():

    # Reads config file
    with open(CONFIGFILE) as infile:
        config_data = json.load(infile)

    mbrecords = get_values(config_data, "mbrecords")

    parsed_records = assign_mbaddress(mbrecords)

    # Writes address assigned records to file
    with open('mbrecords.json', 'w') as outfile:
        json.dump(parsed_records, outfile, indent = 4, sort_keys = True)
        print('Address file created')

    infile.close()
    outfile.close()


if __name__ == "__main__":
    main()