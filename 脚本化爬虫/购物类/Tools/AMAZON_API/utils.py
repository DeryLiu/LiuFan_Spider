import xml.etree.ElementTree as ET
import re

def get_element_by_tag(item,name1,name2=None):
    value = item.getElementsByTagName(name1)
    if len(value) ==0:
        value = ""
    elif name2 is None :
        try:
            value = value[0].childNodes[0].data
        except:
            value =""
    else:
        value = get_element_by_tag(value[0],name2)
    return value