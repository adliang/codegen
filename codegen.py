from templater import template_loop
from mbrecordgen import generate_mblist

def main():

    # Generate modbus database .c file
    tpl_data = generate_mblist('config.json', 'mbrecords.json')
    template_loop('modbusDB.ctpl',  'modbusDB.c', tpl_data)

if __name__ == "__main__":
    main()