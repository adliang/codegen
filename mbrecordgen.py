'''Reads json config file. Returns mb records json file with assigned addresses'''
import json
from pprint import pprint


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


#TODO write default values if record entries are empty / undefined
#TODO allow pre-entered address values in config file.
def assign_mbdata(record_list):
    ''' Assigns addresses to Modbus table. Returns list of of assigned Modbus addresses
        Input: record_list -  Array of entries with dict formatted data'''


    type_len2 = ['U32', 'F32']
    boolean = 'BIT'
    read_write = 'RW'
    read_only = 'RO'
    mbaddress_table = ['0', '1000', '3000', '4000']
    disc_out = 0; disc_in = 1; in_reg = 2; hold_reg = 3
    word_length1 = 1; word_length2 = 2
    mb_list = []

    for record in record_list:
        # Get word length
        if record['type'] in type_len2:
            record['length'] = word_length2
        else:
            record['length'] = word_length1

        # Get table location, set initial address location
        if record['type'] == boolean:
            if record['access'] == read_write:
                table_loc = disc_out
            elif record['access'] == read_only:
                table_loc = disc_in
        else:
            if record['access'] == read_only:
                table_loc = in_reg
            elif record['access'] == read_write:
                table_loc = hold_reg
            else:
                table_loc = hold_reg

        # Get next available table address
        address = mbaddress_table[table_loc]
        next_addr = str(int(mbaddress_table[table_loc]) + record['length'])
        mbaddress_table[table_loc] = next_addr

        record['address'] = address
        mb_list.append(record)

    sorted_list = sorted(mb_list, key=lambda entry: entry['address'])
    return sorted_list


def generate_mblist(config_file, config_key, output_file = None):
    ''' Takes input config_file, returns json list containing entries with assigned addresses'''

    # Reads config file
    with open(config_file) as infile:
        config_data = json.load(infile)
        infile.close()
    global parsed_records
    mbrecords = get_values(config_data, config_key)
    parsed_records = assign_mbdata(mbrecords)

    # Writes address assigned records to file
    if output_file:
        with open(output_file, 'w') as outfile:
            json.dump(parsed_records, outfile, indent = 4)
            outfile.close()
            print('Modbus address list file created')

    return parsed_records

if __name__ == "__main__":
    generate_mblist(config_file = 'config.json', output_file = 'mbrecords.json', config_key = 'mbrecords')