#!/usr/bin/env python
# -*- coding:utf-8 -*-
TAP = "    "


class Attribute(object):
    def __init__(self, name, required, doc, value, type_name, inner_type_name):
        self.name = name
        self.required = required
        self.doc = doc
        self.value = value
        self.type_name = type_name
        self.inner_type_name = inner_type_name


class Content(object):

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
