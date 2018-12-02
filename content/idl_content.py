#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from .content import Content, TAP


class IdlContent(Content):
    """
        Idl文档数据的构建
    """

    def _create_idl_content_by_attrs(self):
        """根据属性栏构建数据"""
        content_list = list()
        for i in range(getattr(self, 'attr_count')):
            attribute = self._get_attribute(i)

            content_line = TAP + str(i + 1) + ": " + attribute.required
            if attribute.type_name == self.current_list_type:
                content_line += " list<" + attribute.inner_type_name + "> "
            else:
                content_line += " " + attribute.type_name + " "
            content_line += attribute.name + ",\n"
            content_list.append(content_line)

        return content_list

    def _create_idl_content_by_text(self):
        """解析文本内容构建数据"""
        text_content = getattr(self, 'text_area').get(1.0, END).split("\n")
        for i in range(len(text_content)):
            attribute = self.__analyse_idl_line(text_content[i])
            if not attribute:
                continue

            getattr(self, 'add_attr')()
            getattr(self, 'attr_names')[i].set(attribute.name)
            self._set_required(i, attribute.required, required_value='required')
            # 设置数值类型
            attr_type = attribute.type_name
            if self.current_list_type in attr_type:
                attr_type = attr_type[attr_type.index('<') + 1: attr_type.index('>')]
                self._set_list_type(i, attr_type)
            else:
                self._set_sole_type(i, attr_type)

    def __analyse_idl_line(self, text_line):
        """解析一行文本"""
        if len(text_line) < 1:  # 当前行没有内容
            return None
        text_line = text_line.split()
        text_line.pop(0)
        result_line = list()
        for text_item in text_line:
            if text_item.endswith(','):
                text_item = text_item[0: len(text_item) - 1]
            result_line.append(text_item)

        attribute = self._get_attribute_from_text(
            result_line,
            name_index=2,
            required_index=0,
            type_name_index=1
        )
        return attribute
