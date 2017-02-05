from templater import template_loop
from mbrecordgen import generate_mblist, assign_mbaddress

def main():

    # Generate modbus database .c file
    generate_mblist('config.json','mbrecords.json', 'mbrecords')
    tpl_data = assign_mbaddress('config.json', 'mbrecords')
    template_loop('modbusDB.ctpl',  'modbusDB.c', tpl_data)

if __name__ == "__main__":
    main()