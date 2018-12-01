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
        if attr_type == 'String':
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
        for i in range(len(text_content)):
            attribute = self.__analyse_model_line(
                text_content[read_index], text_content[read_index + 1])
            read_index += 2
            if not attribute:
                continue

            getattr(self, 'add_attr')()
            getattr(self, 'attr_names')[i].set(attribute.name)
            self._set_required(i, attribute.required, required_value='')
            # 设置数值类型
            attr_bot = attribute.special
            attr_type = attribute.type_name
            if attr_bot == 'Column':
                attr_type = attr_type[0: attr_type.index('(') - 1]
                if attr_type == self.current_list_type:
                    self._set_list_type(i, attr_type)
                else:
                    self._set_sole_type(i, attr_type)
            else:
                if attribute.name.endswith('s'):
                    self._set_list_type(i, attr_type)
                else:
                    self._set_sole_type(i, attr_type)

    def __analyse_model_line(self, first_text_line, second_text_line):
        """解析一行文本"""
        if len(first_text_line) < 1 or len(second_text_line) < 1:  # 当前行没有内容
            return None
        result_line = list()
        first_text_line = first_text_line.split()
        first_text_line.remove('=')
        for text_item in first_text_line:
            if text_item.endswith('('):
                text_item = text_item[0: len(text_item) - 1]
            result_line.append(text_item)
        second_text_line = second_text_line.split()
        for text_item in second_text_line:
            if text_item.endswith(',') or text_item.endswith(')'):
                text_item = text_item[0: len(text_item) - 1]
            result_line.append(text_item)

        attribute = self._get_attribute_from_text(
            result_line,
            name_index=0,
            required_index=5,
            doc_index=3,
            type_name_index=2,
            special_index=1
        )
        return attribute
