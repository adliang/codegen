from templater import template
from mbrecordgen import generate_mblist

def main():

    # Generate modbus database .c file
    tpl_data = generate_mblist()
    template('modbusDB.ctpl',  'modbusDB.c', tpl_data)

if __name__ == "__main__":
    main()