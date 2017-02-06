'''Return 0 if no valid tempalte tags found in tempalte file. Else return 1'''
from pprint import pprint
from string import Template
from mbrecordgen import generate_mblist


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

    # Reads template file
    filetemplate = (open(templatefile)).read()
    header_string, tpl_string, end_string = (split_string(filetemplate, start_tag, end_tag))

    # Loops over template with list data
    text_file = open(outputfile, "w")

    text_file.write(header_string)

    src = Template(tpl_string)
    for entry in tpl_data:
        tpl_filled = src.substitute(entry)
        text_file.write(tpl_filled)

    text_file.write(end_string)

    print('Templating completed')
    text_file.close()
    return 1


if __name__ == "__main__":
    template_loop(templatefile = 'modbusDB.ctpl', outputfile = 'modbusDB.c', tpl_data = generate_mblist('config.json', 'mbrecords'))