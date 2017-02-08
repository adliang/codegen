#!/usr/bin/env python
# ====================================================================== #
'''
templater.py
Generates outputfile using templatefile, looping over [tpl] tags with dict
elements in list input tpl_data
__author__ = Andrew Liang;
'''
# ====================================================================== #

from string import Template

# DELETE - Debugging
from mbrecordgen import generate_mbmap
#


def template_loop(templatefile, outputfile, tpl_data):


    start_tag = '[tpl]'
    end_tag = '[/tpl]'


    # Splits string s into three sections across the first and last tags. Returns array of the three sections
    def split_string(s, first, last):


        if (first not in s) or (last not in s):
            input("No valid template tags in template file. Press enter to continue...")
            return 0
        else:
            return s.partition(first)[0], \
                   s.partition(first)[-1].partition(last)[0], \
                   s.partition(last)[-1]

    # Reads template file, creates output file
    filetemplate = (open(templatefile)).read()
    text_file = open(outputfile, "w")

    # Loops over template with list data
    header_string, tpl_string, end_string = (split_string(filetemplate, start_tag, end_tag))

    text_file.write(header_string)

    src = Template(tpl_string)
    for entry in tpl_data:
        tpl_filled = src.substitute(entry)
        text_file.write(tpl_filled)

    text_file.write(end_string)
    print('(%s) created from %s' %(outputfile, templatefile))
    print('templater.py completed')
    text_file.close()
    return 1

# DELETE - Debugging
if __name__ == "__main__":
    template_loop(templatefile = 'ModbusDB.template.c', outputfile = 'ModbusDB.c', tpl_data = generate_mbmap('config.json', 'mbrecord'))
#