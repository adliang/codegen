#!/usr/bin/env python

import json
import os
import shutil
import sys
import copy
sys.path.append('.')
import ipc

# Use following to find all types and number of occurances with:
# cat ../../../config.json | grep 'type' | sed -e 's/^[[:space:]]*//' | sort | uniq -c
typesizes = {
    "c_bool": 1,
    "c_short":1,
    "c_ushort": 1,
    "c_int": 2,
    "c_uint": 2,
    "c_float": 2,
    "c_ulong": 4,
    "LP_c_float": 2,                # ignored (in buttons)
    "LP_phasetable_entry_t":2,      # ignored
    "vector2_t":4,
    # "c_ubyte": 1,                 do not use
}


def getdict(struct,name_in=None,varprefix="", access='RO'):
    result = {}
    for field,ctype in struct._fields_:
         val = getattr(struct, field)
                
         if name_in == None:
             name = field
         else:
             name = name_in + '.' + field
         
         # HACK
         acc = copy.copy(access)
         if field == "Settings":
             acc = "RW"
         
         # Ignore branches and variables starting with _
         if not field.startswith('_'):
            ignore = False
            if hasattr(val, "_fields_") and not ignore:
                # Probably another struct.. so recurse
                value = getdict(val, name, varprefix, acc)
            else:
                # If Array it'll contain a _length_ field, and we multipy by array size
                arraylen = 1
                if hasattr(val, "_length_") and hasattr(val, "_type_"):
                    arraylen = val._length_
                    ctype = val._type_

                if str(ctype.__name__).startswith("LP_"):
                    print("      Ignoring long pointer type: " + ctype.__name__)
                    ignore = True
                
                # Look-up type size            
                if typesizes.has_key(ctype.__name__):
                    typesize = typesizes[ctype.__name__]
                else:
                    print("      Ignoring unknown type: " + ctype.__name__)
                    ignore = True
                
                varname = varprefix + '.' + name
                varwrite = "NULL"
                if access == "RW":
                    varwrite = '&(ipc_MtoC.' + name + ')'
                    
                if not ignore:
                    value = {"mbrecord":
                                {
                                'name':field,
                                'length':arraylen * typesize,
                                'type': ctype.__name__,
                                'varname': varname,
                                'varwrite': varwrite,
                                'access': access
                                }
                            }
                else:
                    value = {"mbrecord":
                                {
                                'name':field,
                                'varname': varname,
                                'ignore': True
                                }
                            }
            result[field] = value
    return result

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                path.append(key)
                keyname = ".".join(str(x) for x in path)
                print("      Warning!! Overriding key: " + keyname + " = "+ repr(a[key]) + " => " + repr(b[key]))
                a[key] = b[key]
        else:
            a[key] = b[key]
    return a


print("CONFIG GEN")

ipc = ipc.ipc_core_to_master_t()

configfile = '../../../config.json'
configuserfile = '../../../config-user.json'
configbakfile = configfile + '-configgenbackup'
configfreshfile = configfile + '-fresh'

print('   Processing...')
cfg_fresh = {}
cfg_fresh.update( {'Ipc':getdict(ipc, name_in=None, varprefix="ipc_CtoM")} )
#cfg_fresh.update( {'Measurements':getdict(measurements, name="Measurements", access='RO')} )
cfg_fresh.update( {'Types':{'Sizes':typesizes}})

print('   Created fresh as: ' + configfreshfile)
with open(configfreshfile, 'w') as outfile:
    json.dump(cfg_fresh, outfile, sort_keys=True,indent=4, separators=(',', ': '))

cfg_orig = {}
cfg_user = {}
if os.path.isfile (configfile):
    print('   Saving back-up as: ' + configbakfile)
    shutil.copyfile(configfile, configbakfile)

    with open(configfile) as jsonfile:
        cfg_orig = json.load(jsonfile)

if os.path.isfile (configuserfile):
    with open(configuserfile) as jsonfile:
        cfg_user = json.load(jsonfile)

print('   Merging...')
cfg_merged = merge(cfg_orig, cfg_fresh)
cfg_merged = merge(cfg_merged, cfg_user)

print('   Saving merged as: ' + configfile)
with open(configfile, 'w') as outfile:
    json.dump(cfg_merged, outfile, sort_keys=True,indent=4, separators=(',', ': '))

print('Done.')
