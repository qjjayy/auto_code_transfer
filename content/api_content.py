#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from TType import *


class APIContent(object):
    """
        API文档数据的构建
    """
    def _create_api_content_by_attrs(self):
        """根据属性栏构建数据"""
        content_list = list()
        for i in range(getattr(self, 'attr_count')):
            if getattr(self, 'attr_requireds')[i].get() == 'True':
                required = "required"
            else:
                required = "optional"

            if getattr(self, 'attr_values')[i].get() != '':
                value_name = ': ' + getattr(self, 'attr_values')[i].get()
            else:
                value_name = ' '

            if getattr(self, 'attr_nest_types')[i].get() != '':
                type_name = getattr(self, 'attr_nest_types')[i].get()
            else:
                type_name = getattr(self, 'attr_types')[i].get().split('_')[0]

            if type_name == "array":
                if getattr(self, 'attr_inner_nest_types')[i].get() != '':
                    inner_type_name = getattr(self, 'attr_inner_nest_types')[i].get()
                else:
                    inner_type_name = getattr(self, 'attr_inner_types')[i].get().split('_')[0]

                content_list.append("+ " + getattr(self, 'attr_names')[i].get() +
                                    value_name + " (array[" + inner_type_name + "], " + required +
                                    ") - " + getattr(self, 'attr_docs')[i].get() + "\n")
            else:
                content_list.append("+ " + getattr(self, 'attr_names')[i].get() +
                                    value_name + " (" + type_name + ", " + required +
                                    ") - " + getattr(self, 'attr_docs')[i].get() + "\n")
        return content_list

    def _create_api_content_by_text(self):
        text_content = getattr(self, 'text_area').get(1.0, END).split("\n")
        for i in range(len(text_content)):
            text_line = self.__extract_api_line(text_content[i])
            if not text_line:
                continue

            getattr(self, 'add_attr')()

            if len(text_line) == 5:
                getattr(self, 'attr_values')[i].set(text_line.pop(1))
            getattr(self, 'attr_names')[i].set(text_line[0])

            attr_type = text_line[1]
            if 'array' in attr_type:
                attr_type = attr_type[attr_type.index('[') + 1: attr_type.index(']')]
                getattr(self, 'attr_types')[i].set('array')
                getattr(self, 'entry_inner_types')[i]['state'] = NORMAL
                getattr(self, 'inner_type_button')['state'] = NORMAL
                self.__set_type(i, attr_type, 5, 'inner_')
            else:
                self.__set_type(i, attr_type, 4)

            if text_line[2] == 'required':
                getattr(self, 'attr_requireds')[i].set('True')
            else:
                getattr(self, 'attr_requireds')[i].set('False')
            getattr(self, 'attr_docs')[i].set(text_line[3])

    def __set_type(self, i, attr_type, type_column, type_name=''):
        if attr_type in RealAPIType:
            if attr_type == 'number':
                attr_type = 'number_int'
            getattr(self, 'attr_%stypes' % type_name)[i].set(attr_type)
            getattr(self, 'entry_%snest_types' % type_name)[i].grid_remove()
            getattr(self, 'entry_%stypes' % type_name)[i].grid(row=i + 1, column=type_column)
        else:
            getattr(self, 'attr_%snest_types' % type_name)[i].set(attr_type)
            getattr(self, 'entry_%stypes' % type_name)[i].grid_remove()
            getattr(self, 'entry_%snest_types' % type_name)[i].grid(row=i + 1, column=type_column)

    def __extract_api_line(self, text_line):
        if len(text_line) < 1:
            return None
        text_line = text_line.split()
        text_line.remove('+')
        text_line.remove('-')
        result_line = list()
        for text_item in text_line:
            text_item = list(text_item)
            if ':' in text_item and text_item.index(':') == len(text_item) - 1:
                text_item.remove(':')
            elif '(' in text_item and ',' in text_item and \
                    text_item.index('(') == 0 and text_item.index(',') == len(text_item) - 1:
                text_item.remove('(')
                text_item.remove(',')
            elif ')' in text_item and '(' not in text_item and \
                    text_item.index(')') == len(text_item) - 1:
                text_item.remove(')')
            text_item = ''.join(text_item)
            result_line.append(text_item)
        return result_line