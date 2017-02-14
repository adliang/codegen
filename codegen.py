#!/usr/bin/env python

from templater import template_loop
from mbrecordgen import generate_mbmap, pdfgen


def main():
    print("\nCODEGEN of ModbusDB.c")
    # Generate modbus database .c file
    tpl_data = generate_mbmap('../../../config.json', 'mbrecord', 'Mbrecords.json')
    pdfgen(tpl_data, '../../../Documentation/ModbusRecords.pdf')

    template_loop('../secheron/Modbus/ModbusDB.template.c',  '../secheron/Modbus/ModbusDB.c', tpl_data)
    print ("Done.\n")

if __name__ == "__main__":
    main()