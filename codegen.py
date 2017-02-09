from templater import template_loop
from mbrecordgen import generate_mbmap
from prettytable import PrettyTable, ALL, FRAME, HEADER
from PDFWriter import PDFWriter


def main():

    # Generate modbus database .c file
    tpl_data = generate_mbmap('config.json', 'mbrecord', 'Mbrecords.json')
    template_loop('ModbusDB.template.c',  'ModbusDB_test.c', tpl_data)


    pt = PrettyTable(["PDU Address", "varname", "type", "access", "length"])
    pt.align = "l"
    pt.hrules = HEADER
    for i in range(0, len(tpl_data)):
        pt.add_row([tpl_data[i]['address'],tpl_data[i]['varname'],tpl_data[i]['type'],tpl_data[i]['access'],tpl_data[i]['length']])
    lines = pt.get_string()
    pw = PDFWriter('Modbus Records.pdf')
    pw.setFont('Courier', 8)
    pw.setHeader('Modbus records')
    pw.setFooter('Modbus records')
    for line in lines.split('\n'):
        pw.writeLine(line)
    pw.close()

if __name__ == "__main__":
    main()