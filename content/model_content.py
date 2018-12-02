#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from TType import *
from .content import Content, TAP


class ModelContent(Content):
    """
        Model数据的构建
    """

    def _create_model_content_by_attrs(self):
        """根据属性栏构建数据"""
        content_list = list()
        for i in range(getattr(self, 'attr_count')):
            attribute = self._get_attribute(i)

            content_line = TAP + attribute.name + " = "
            if attribute.type_name not in ModelTypes:
                content_line += "relationship(\n" + TAP + TAP + attribute.type_name + ")\n"
            elif attribute.inner_type_name not in ModelTypes:
                content_line += "relationship(\n" + TAP + TAP + attribute.inner_type_name + ")\n"
            else:
                content_line += "Column(\n" + TAP + TAP + \
                                self.__get_model_specific_attr_type(attribute.type_name) + \
                                ", doc=u'" + attribute.doc + "', nullable=False"
                if attribute.required == 'required':
                    content_line += ")\n"
                else:
                    content_line += ", default=" + self.__get_model_missing(attribute.type_name) + ")\n"
            content_list.append(content_line)

        return content_list

    def __get_model_specific_attr_type(self, attr_type):
        """获取展示类型"""
        if attr_type == 'String':
            return "String(255)"
        elif attr_type == 'ChoiceType':
            return "ChoiceType()"
        elif attr_type == 'Numeric':
            return "Numeric(precision=11, scale=3)"
        elif attr_type == 'ScalarListType':
            return "ScalarListType(unicode)"
        elif attr_type == 'ArrowType':
            return "ArrowType()"
        else:
            return attr_type

    def __get_model_missing(self, attr_type):
        """获取默认值"""
        if attr_type == 'String' or 'ChoiceType':
            return "u''"
        elif attr_type == 'Boolean':
            return "False"
        elif attr_type == 'ScalarListType':
            return "[]"
        else:
            return "0"

    def _create_model_content_by_text(self):
        """解析文本内容构建数据"""
        read_index = 0
        text_content = getattr(self, 'text_area').get(1.0, END).split("\n")
        for write_index in range(len(text_content)):
            content_lines = [text_content[read_index]]
            while (len(text_content[read_index]) > 1 and
                    not text_content[read_index].endswith(')')):
                read_index += 1
                content_lines.append(text_content[read_index])

            attribute = self.__analyse_model_line(content_lines)
            if not attribute:
                continue

            getattr(self, 'add_attr')()
            getattr(self, 'attr_names')[write_index].set(attribute.name)
            getattr(self, 'attr_docs')[write_index].set(attribute.doc)
            self._set_required(write_index, attribute.required, required_value='True')
            # 设置数值类型
            attr_bot = attribute.special
            attr_type = attribute.type_name
            if attr_bot == 'Column':
                if attr_type == self.current_list_type:
                    attr_type = 'String'
                    self._set_list_type(write_index, attr_type)
                else:
                    self._set_sole_type(write_index, attr_type)
            else:
                if attribute.name.endswith('s'):
                    self._set_list_type(write_index, attr_type)
                else:
                    self._set_sole_type(write_index, attr_type)

            read_index += 1
            if read_index > len(text_content) - 1:
                break

    def __analyse_model_line(self, content_lines):
        """解析一行文本"""
        result_line = list()
        for content_line in content_lines:
            if len(content_line) < 1:
                return None
        # 拼接多行
        text_line = ''
        for content_line in content_lines:
            text_line += content_line
        pre_line = text_line[0: text_line.index('(')]
        config_line = text_line[text_line.index('(') + 1: -1]
        # 数值名
        pre_line = pre_line.split()
        result_line.append(pre_line[0])
        # 特殊数值类型
        result_line.append(pre_line[2])
        # 数值类型
        config_line = config_line.split(',')
        type_name = config_line.pop(0)
        type_name = type_name.replace(' ', '')
        if '(' in type_name:
            type_name = type_name[0: type_name.index('(')]
        result_line.append(type_name)
        # 数值doc和required
        doc = ''
        required = 'True'
        for text in config_line:
            if 'doc' in text:
                start_index = text.index('\'')
                doc = text[start_index + 1: text.index('\'', start_index + 1)]
            elif 'default' in text:
                required = 'False'
        result_line.append(doc)
        result_line.append(required)

        attribute = self._get_attribute_from_text(
            result_line,
            name_index=0,
            required_index=4,
            doc_index=3,
            type_name_index=2,
            special_index=1
        )
        return attribute
