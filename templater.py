from pprint import pprint
from string import Template

# TODO rewrite as class
# Splits string s into three sections across the first and last tags. Returns array of the three sections
def split_string(s, first, last):

    try:
        return s.partition(first)[0], \
               s.partition(first)[-1].partition(last)[0], \
               s.partition(last)[-1]
    except ValueError:
        return "No valid template tags found"


def template(templatefile, outputfile, tpl_data):


    start_tag = '[tpl]'
    end_tag = '[/tpl]'

    # Reads template file
    filetemplate = (open(templatefile)).read()
    header_string, tpl_string, end_string = (split_string(filetemplate,start_tag,end_tag))

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



if __name__ == "__main__":
    template(templatefile = 'modbusDB.ctpl', outputfile = 'modbusDB.c')