#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from TType import SchemaTypes
from collections import OrderedDict
TAP = "    "


class SchemaContent(object):
    def _create_schema_content_by_attrs(self):
        content_list = list()
        for i in range(getattr(self, 'attr_count')):

            attr_name = getattr(self, 'attr_names')[i].get()

            if getattr(self, 'attr_nest_types')[i].get() != '':
                type_name = getattr(self, 'attr_nest_types')[i].get()
            else:
                type_name = getattr(self, 'attr_types')[i].get()

            if type_name == "List":
                if getattr(self, 'attr_inner_nest_types')[i].get() != '':
                    content_str = attr_name + " = fields.Nested(" + \
                        getattr(self, 'attr_inner_nest_types')[i].get() + ", many=True, required="
                else:
                    content_str = attr_name + " = fields.List(fields." + \
                        getattr(self, 'attr_inner_types')[i].get() + "(), required="
            elif type_name == "Decimal":
                content_str = attr_name + " = fields.Decimal(places=3" + ", required="
            elif type_name in SchemaTypes:
                content_str = attr_name + " = fields." + type_name + "(required="
            else:
                content_str = attr_name + " = fields.Nested(" + type_name + "Schema, required="

            if getattr(self, 'attr_requireds')[i].get() == 'True':
                content_list.append(TAP + content_str + "True, allow_none=False)\n")
            else:
                content_list.append(TAP + content_str + "False, missing="
                                    + self.__get_schema_missing(type_name) + ")\n")

        return content_list

    def __get_schema_missing(self, type_name):
        if type_name == "Str":
            return "u''"
        elif type_name == "Bool":
            return "False"
        elif type_name == "List":
            return "[]"
        elif type_name in SchemaTypes:
            return "0"
        else:
            return "None"

    def _create_schema_content_by_text(self):
        text_content = getattr(self, 'text_area').get(1.0, END).split("\n")
        for row in range(len(text_content)):
            result_dict = self.__extract_schema_line(text_content[row])
            if not result_dict:
                continue
            print result_dict

            getattr(self, 'add_attr')()

            getattr(self, 'attr_names')[row].set(result_dict['attr_name'])

            type_name = result_dict['type_name']
            inner_type_name = result_dict.get('inner_type_name')
            if type_name == 'Nested':
                if result_dict.get('many', False):
                    getattr(self, 'inner_type_button')['state'] = NORMAL
                    getattr(self, 'entry_inner_types')[row]['state'] = NORMAL
                    self.__set_type(row, getattr(self, 'type_column'), 'List')
                    self.__set_type(row, getattr(self, 'inner_type_column'), inner_type_name, 'inner_')
                else:
                    self.__set_type(row, getattr(self, 'type_column'), inner_type_name)
            elif type_name == 'List':
                getattr(self, 'inner_type_button')['state'] = NORMAL
                getattr(self, 'entry_inner_types')[row]['state'] = NORMAL
                self.__set_type(row, getattr(self, 'type_column'), 'List')
                self.__set_type(row, getattr(self, 'inner_type_column'), inner_type_name, 'inner_')
            else:
                self.__set_type(row, getattr(self, 'type_column'), type_name)

            if result_dict.get('required', 'False') == 'True':
                getattr(self, 'attr_requireds')[row].set('True')
            else:
                getattr(self, 'attr_requireds')[row].set('False')

    def __set_type(self, row, column, type_name, is_inner=''):
        if type_name in getattr(self, 'get_types')()[0]:
            getattr(self, 'attr_%snest_types' % is_inner)[row].set('')
            getattr(self, 'attr_%stypes' % is_inner)[row].set(type_name)
            getattr(self, 'entry_%snest_types' % is_inner)[row].grid_remove()
            getattr(self, 'entry_%stypes' % is_inner)[row].grid(row=row + 1, column=column)
        else:
            getattr(self, 'entry_%stypes' % is_inner)[row].current(0)
            getattr(self, 'attr_%snest_types' % is_inner)[row].set(type_name)
            getattr(self, 'entry_%stypes' % is_inner)[row].grid_remove()
            getattr(self, 'entry_%snest_types' % is_inner)[row].grid(row=row + 1, column=column)

    def __extract_schema_line(self, text_line):
        if len(text_line) < 1:
            return None
        text_line = text_line.split()
        result_dict = OrderedDict()
        content = ''
        for i in range(2, len(text_line)):
            content += text_line[i]
        first_index = content.index('(')
        config = content[first_index + 1: -1].split(',')

        result_dict['attr_name'] = text_line[0]
        result_dict['type_name'] = content[7: first_index]
        for config_item in config:
            if '=' not in config_item:
                if '.' in config_item and '(' in config_item:
                    first_index = config_item.index('.')
                    last_index = config_item.index('(')
                    result_dict['inner_type_name'] = config_item[first_index + 1: last_index]
                else:
                    result_dict['inner_type_name'] = config_item
            else:
                split_index = config_item.index('=')
                result_dict[config_item[0: split_index]] = config_item[split_index + 1:]

        return result_dict
