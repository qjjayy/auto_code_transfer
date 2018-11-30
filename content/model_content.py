#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from TType import *
from .content import Content


class ModelContent(Content):
    """
        Model数据的构建
    """

    def _create_model_content_by_attrs(self):
        """根据属性栏构建数据"""
        content_list = list()
        for i in range(getattr(self, 'attr_count')):
            attribute = self._get_attribute(i)

            content_line = self.TAP + attribute.name + " = "
            if attribute.inner_type_name not in ModelTypes:
                content_line += "relationship(\n" + self.TAP + self.TAP + \
                                "\"" + attribute.inner_type_name + "\")\n"
            else:
                content_line += "Column(\n" + self.TAP + self.TAP + \
                                self.__get_model_specific_attr_type(attribute.type_name) + \
                                ", doc=u'" + attribute.doc + "', nullable=False"
                if attribute.required == 'True':
                    content_line += ")\n"
                else:
                    content_line += ", default=" + self.__get_model_missing(attribute.type_name) + ")\n"
            content_list.append(content_line)

        return content_list

    def __get_model_specific_attr_type(self, attr_type):
        """获取展示类型"""
        if attr_type == str(ModelTType.String):
            return "String(255)"
        elif attr_type == str(ModelTType.Numeric):
            return "Numeric(precision=11, scale=3)"
        elif attr_type == str(ModelTType.ScalarListType):
            return "ScalarListType(unicode)"
        elif attr_type == str(ModelTType.ArrowType):
            return "ArrowType()"
        else:
            return attr_type

    def __get_model_missing(self, attr_type):
        """获取默认值"""
        if attr_type == str(ModelTType.String):
            return "u''"
        elif attr_type == str(ModelTType.Boolean):
            return "False"
        elif attr_type == str(ModelTType.ScalarListType):
            return "[]"
        else:
            return "0"

