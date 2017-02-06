from templater import template_loop
from mbrecordgen import generate_mbmap
from pprint import pprint

def main():

    # Generate modbus database .c file
    tpl_data = generate_mbmap('config.json', 'mbrecords', 'mbrecords.json')
    template_loop('modbusDB.ctpl',  'modbusDB.c', tpl_data)
    pprint(tpl_data)

if __name__ == "__main__":
    main()