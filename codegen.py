from templater import template_loop
from mbrecordgen import generate_mbmap
from pprint import pprint
from csv import DictWriter

def main():

    # Generate modbus database .c file
    tpl_data = generate_mbmap('config_test.json', 'mbrecord', 'Mbrecords_test.json')
    template_loop('ModbusDB.template.c',  'ModbusDB_test.c', tpl_data)
    #pprint(tpl_data)


    # Testing excel output code
    '''
    table_data = {}

    for i in range(0, len(tpl_data)):
        table_data.update({tpl_data[i]['address'] : tpl_data[i]})


    for key in table_data:
        del table_data[key]['address']


    #pprint(table_data)

    t = PrettyTable(['key', 'value'])
    for key, val in table_data.items():
        t.add_row([key, val])
    print(t)

    with open("thing.pdf", 'w') as outfile:
        text_file = open(outfile, "w")
        text_file.write(t)'''
        #for key, val in sorted(table_data):
      #  table.add_column(key, sorted(val))

    #print(table)
    #pprint(tpl_data)
    #print(table)
    #input("Code generation completed. Press enter to continue...")

if __name__ == "__main__":
    main()