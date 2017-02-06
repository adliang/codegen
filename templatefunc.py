from mbrecordgen import generate_mblist
from pprint import pprint
from string import Template



TEMPLATEFILE = 'modbusDB.ctpl'
start_tag = '[tpl]'
end_tag = '[/tpl]'

# Splits string s into three sections across the first and last tags. Returns array of the three sections
def split_string(s, first, last):

    try:
        return s.partition(first)[0], \
               s.partition(first)[-1].partition(last)[0], \
               s.partition(last)[-1]
    except ValueError:
        return "No valid template tags found"


def ():


    # Reads template file
    filetemplate = (open(TEMPLATEFILE)).read()
    header_string, tpl_string, end_string = (split_string(filetemplate,start_tag,end_tag))

    text_file = open("modbusDB.c", "w")
    text_file.write(header_string)

    src = Template(tpl_string)

    tpl_data = generate_mblist()
    for entry in tpl_data:
        tpl_filled = src.substitute(entry)
        print(tpl_filled)
        text_file.write(tpl_filled)

    text_file.write(end_string)

    text_file.close()

if __name__ == "__main__":
    main()