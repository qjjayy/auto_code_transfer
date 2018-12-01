#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from TType import *
from .content import Content, TAP
from collections import OrderedDict


class SchemaContent(Content):
    """
        Schema数据的构建
    """

    def _create_schema_content_by_attrs(self):
        """根据属性栏构建数据"""
        content_list = list()
        for i in range(getattr(self, 'attr_count')):
            attribute = self._get_attribute(i)

            content_line = TAP + attribute.name + " = fields."
            if attribute.type_name == 'List':
                if attribute.inner_type_name not in SchemaTypes:
                    content_line += "Nested(" + attribute.inner_type_name + ", many=True, "
                else:
                    content_line += "List(fields." + attribute.inner_type_name + "(), "
            elif attribute.type_name in SchemaTypes:
                content_line += attribute.type_name + "("
            else:
                content_line += "Nested(" + attribute.type_name + "Schema, "

            if attribute.required == 'required':
                content_line += "required=True, allow_none=False)\n"
            else:
                content_line += "required=False, missing=" + \
                                self.__get_schema_missing(attribute.type_name) + ")\n"
            content_list.append(content_line)

        return content_list

    def __get_schema_missing(self, type_name):
        """获取默认值"""
        if type_name == 'Str':
            return "u''"
        elif type_name == 'Bool':
            return "False"
        elif type_name == 'List':
            return "[]"
        elif type_name in SchemaTypes:
            return "0"
        else:
            return "None"

    def _create_schema_content_by_text(self):
        """解析文本内容构建数据"""
        text_content = getattr(self, 'text_area').get(1.0, END).split("\n")
        read_index = 0
        for write_index in range(len(text_content)):
            content_lines = [text_content[read_index]]
            while not text_content[read_index + 1].endswith(')'):
                read_index += 1
                content_lines.append(text_content[read_index])

            attribute = self.__extract_schema_line(content_lines)
            if not attribute:
                continue

            getattr(self, 'add_attr')()
            getattr(self, 'attr_names')[write_index].set(attribute.name)
            self._set_required(write_index, attribute.required, required_value='True')
            # 设置数值类型
            attr_type = attribute.type_name
            if attr_type == 'Nested':
                attr_special = attribute.special
                attr_type = attr_special[0: attr_special.index('Schema')]
                if 'many=True' in attribute.special:
                    self._set_list_type(write_index, attr_type)
                else:
                    self._set_sole_type(write_index, attr_type)
            elif attr_type == self.current_list_type:
                attr_special = attribute.special
                attr_type = attr_special[attr_special.index('.') + 1: attr_special.index('(')]
                self._set_list_type(write_index, attr_type)
            else:
                self._set_sole_type(write_index, attr_type)

    def __extract_schema_line(self, content_lines):
        """解析一行文本"""
        result_line = list()
        for content_line in content_lines:
            if len(content_line) < 1:
                return None
        # 拼接多行
        text_line = ''
        for content_line in content_lines:
            text_line += content_line
        # 数值名
        text_line = text_line.split()
        result_line.append(text_line[0])
        # 数值类型
        field = text_line.pop(2)
        type_name = field[0: field.index('(')].split('.')[1]
        result_line.append(type_name)
        # 特殊数值类型
        configs = field[field.index('(') + 1: -1].split(',')
        if '=' not in configs[0]:
            special = configs[0].replace('\n', '').replace(' ', '')
        else:
            special = ''
        # 数值required
        required = 'False'
        for config in configs:
            if 'required=True' in config:
                required = 'True'
            elif 'many=True' in config:
                special += ',' + config
        result_line.append(required)
        result_line.append(special)

        attribute = self._get_attribute_from_text(
            result_line,
            name_index=0,
            required_index=2,
            type_name_index=1,
            special_index=3
        )
        return attribute
