#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from TType import *
from .content import Content


class IdlContent(Content):
    """
        Idl文档数据的构建
    """

    def _create_idl_content_by_attrs(self):
        """根据属性栏构建数据"""
        content_list = list()
        for i in range(getattr(self, 'attr_count')):
            attribute = self._get_attribute(i)

            content_line = self.TAP + str(i + 1) + ": " + attribute.required
            if attribute.type_name == str(IdlTType.list):
                content_line += " list<" + attribute.inner_type_name + "> "
            else:
                content_line += " " + attribute.type_name + " "
            content_line += attribute.name + ",\n"
            content_list.append(content_line)

        return content_list
