# Вариант 27
from lark import Lark, visitors
from xml.etree.ElementTree import Element, tostring
from xml.dom import minidom

grammar = r""" 
start: value+

NUM: /0[xX][0-9a-fA-F]+/
STR: /@"[^"]+"/
NAME: /[_a-zA-Z][_a-zA-Z0-9]*/

assign: NAME ":" value
dict: "([" (assign ",")+ "])"
value: NUM | STR | dict 

%ignore /\s/  
%ignore /\{[^}]+\}/ 
     
"""

class T(visitors.Transformer):
    NUM = str
    STR = str
    NAME = str
    
    def start(self, values):
        root = Element('root')
        for value in values:
            if isinstance(value, dict):
                dict_elem = Element('dict')
                for k, v in value.items():
                    item_elem = Element('item')
                    key_elem = Element('key')
                    key_elem.text = k
                    value_elem = Element('value')
                    if isinstance(v, dict):

                        nested_dict = self._dict_to_xml(v, Element('dict'))
                        value_elem.append(nested_dict)
                    else:
                        value_elem.text = v
                    item_elem.append(key_elem)
                    item_elem.append(value_elem)
                    dict_elem.append(item_elem)
                root.append(dict_elem)
            else:
                value_elem = Element('value')
                value_elem.text = value
                root.append(value_elem)
        return root
    
    def _dict_to_xml(self, d, elem):
        for k, v in d.items():
            item_elem = Element('item')
            key_elem = Element('key')
            key_elem.text = k
            value_elem = Element('value')
            if isinstance(v, dict):
                nested_dict = self._dict_to_xml(v, Element('dict'))
                value_elem.append(nested_dict)
            else:
                value_elem.text = v
            item_elem.append(key_elem)
            item_elem.append(value_elem)
            elem.append(item_elem)
        return elem
    
    def assign(self, items):
        return (items[0], items[1])
    
    def dict(self, items):
        return dict(items)
    
    def value(self, items):
        return items[0]

def prettify_xml(elem):
    """Возвращает красиво отформатированную XML-строку"""
    rough_string = tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

input = """
{ Это многострочный комментарий}
{
Это многострочный
комментарий
}
0X5576AD
0x5657ade
([
   A : 0XCAFE,
   C : @"Stroka",
])
"""
parser = Lark(grammar)
tree = parser.parse(input)
tree = T(visit_tokens=True).transform(tree)

xml_output = prettify_xml(tree)
print(xml_output)