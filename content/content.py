#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
TAP = "    "


class Attribute(object):
    def __init__(self, name, required, doc, value,
                 type_name, inner_type_name, special=None):
        self.name = name
        self.required = required
        self.doc = doc
        self.value = value
        self.type_name = type_name
        self.inner_type_name = inner_type_name
        self.special = special


class Content(object):

    @property
    def current_list_type(self):
        return getattr(self, 'current_data_type')[4]

    def _get_attribute(self, index):
        """获取当前数据的属性"""
        name = getattr(self, 'attr_names')[index].get()

        if getattr(self, 'attr_requireds')[index].get() == 'True':
            required = "required"
        else:
            required = "optional"

        doc = getattr(self, 'attr_docs')[index].get()

        value = getattr(self, 'attr_values')[index].get()

        if getattr(self, 'attr_nest_types')[index].get() != '':
            type_name = getattr(self, 'attr_nest_types')[index].get()
        else:
            type_name = getattr(self, 'attr_types')[index].get().split('_')[0]

        if getattr(self, 'attr_inner_nest_types')[index].get() != '':
            inner_type_name = getattr(self, 'attr_inner_nest_types')[index].get()
        else:
            inner_type_name = getattr(self, 'attr_inner_types')[index].get().split('_')[0]

        return Attribute(name, required, doc, value, type_name, inner_type_name)

    def _get_attribute_from_text(
            self, result_line, name_index=None, required_index=None, doc_index=None,
            value_index=None, type_name_index=None, inner_type_name_index=None,
            special_index=None):
        """获取当前文本行的数据属性"""
        try:
            name = result_line[name_index]
        except Exception as exc:
            name = ''

        try:
            required = result_line[required_index]
        except Exception as exc:
            required = ''

        try:
            doc = result_line[doc_index]
        except Exception as exc:
            doc = ''

        try:
            value = result_line[value_index]
        except Exception as exc:
            value = ''

        try:
            type_name = result_line[type_name_index]
        except Exception as exc:
            type_name = ''

        try:
            inner_type_name = result_line[inner_type_name_index]
        except Exception as exc:
            inner_type_name = ''

        try:
            special = result_line[special_index]
        except Exception as exc:
            special = ''

        return Attribute(name, required, doc, value, type_name, inner_type_name, special)

    def _set_list_type(self, i, attr_type):
        """设置数值列表类型"""
        getattr(self, 'attr_types')[i].set(self.current_list_type)
        getattr(self, 'entry_inner_types')[i]['state'] = NORMAL
        getattr(self, 'inner_type_button')['state'] = NORMAL
        self.__set_type(i, attr_type, getattr(self, 'inner_type_column'), 'inner_')

    def _set_sole_type(self, i, attr_type):
        """设置数据单独类型"""
        self.__set_type(i, attr_type, getattr(self, 'type_column'))

    def _set_required(self, i, required, required_value):
        """设置数据的必须属性"""
        if required == required_value:
            getattr(self, 'attr_requireds')[i].set('True')
        else:
            getattr(self, 'attr_requireds')[i].set('False')

    def __set_type(self, i, attr_type, type_column, is_inner=''):
        """设置数值类型"""
        if attr_type in getattr(self, 'current_data_type'):
            getattr(self, 'attr_%stypes' % is_inner)[i].set(attr_type)
            getattr(self, 'attr_%snest_types' % is_inner)[i].set('')
            getattr(self, 'entry_%snest_types' % is_inner)[i].grid_remove()
            getattr(self, 'entry_%stypes' % is_inner)[i].grid(row=i + 1, column=type_column)
        else:
            getattr(self, 'attr_%snest_types' % is_inner)[i].set(attr_type)
            getattr(self, 'entry_%stypes' % is_inner)[i].current(0)
            getattr(self, 'entry_%stypes' % is_inner)[i].grid_remove()
            getattr(self, 'entry_%snest_types' % is_inner)[i].grid(row=i + 1, column=type_column)

