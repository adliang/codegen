from templater import template_loop
from mbrecordgen import generate_mbmap


def main():

    # Generate modbus database .c file
    tpl_data = generate_mbmap('config.json', 'mbrecord', 'Mbrecords.json')
    template_loop('ModbusDB.template.c',  'ModbusDB_test.c', tpl_data)

if __name__ == "__main__":
    main()