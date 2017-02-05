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


# Assigns addresses to Modbus table. Returns list of of assigned Modbus addresses
#TODO get rid of magic numbers
def assign_mbaddress(config_file, config_key):


    # Reads config file
    with open(config_file) as infile:
        config_data = json.load(infile)
        infile.close()
    record_list = get_values(config_data, config_key)

    word_len_2 = ['U32', 'F32']
    boolean = 'BIT'
    read_write = 'RW'
    read_only = 'RO'
    offset = 1000   # Offset between modbus register addresses
    mb_list = []

    for record in record_list:
        # Get word length
        if record['type'] in word_len_2:
            record['length'] = 2
        else:
            record['length'] = 1
        # Get table location, set initial address location
        if record['type'] == boolean:
            if record['access'] == read_write:
                address = '0'
            elif record['access'] == read_only:
                address = '1000'
        else:
            if record['access'] == read_only:
                address = '3000'
            elif record['access'] == read_write:
                address = '4000'

        # Get next available table address
        if any(entry['address'] == address for entry in mb_list):
            max_address = max(int(entry['address']) for entry in mb_list if int(entry['address']) < int(address) + offset)
            prev_length = max((entry['length']) for entry in mb_list if (entry['address']) == str(max_address))
            address = str(max_address +  prev_length)

        record['address'] = address
        mb_list.append(record)

    sorted_list = sorted(mb_list, key=lambda entry: entry['address'])
    return sorted_list


# Takes input config_file, returns json list containing entries with assigned addresses
def generate_mblist(config_file, output_file, config_key):


    # Reads config file
    with open(config_file) as infile:
        config_data = json.load(infile)
        infile.close()

    mbrecords = get_values(config_data, config_key)
    parsed_records = assign_mbaddress(config_file, config_key)
    pprint(parsed_records)

    # Writes address assigned records to file
    with open(output_file, 'w') as outfile:
        json.dump(parsed_records, outfile, indent = 4)
        outfile.close()

    print('Modbus address list file created')

if __name__ == "__main__":
    generate_mblist(config_file = 'config.json', output_file = 'mbrecords.json', config_key = 'mbrecords')