#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from TType import *
from content import Content


class PageConfig(Content):

    def __init__(self, root):
        # 适配各Schema层中的特殊对应
        self.input_float = list()
        self.output_float = list()
        self.object_float = list()
        self.inner_input_float = list()
        self.inner_output_float = list()
        self.inner_object_float = list()
        # 页面属性配置
        self.page_type_config = {
            "api": [APITypes, None, None],
            "schema_input": [SchemaTypes, self.input_float, self.inner_input_float],
            "schema_output": [SchemaTypes, self.output_float, self.inner_output_float],
            "idl": [IdlTypes, None, None],
            "schema_object": [SchemaTypes, self.object_float, self.inner_object_float],
            "model": [ModelTypes, None, None],
            "request": [None, None, None]
        }

        for key, value in self.page_type_config.items():
            self.page_type_config[key].append(getattr(self, '_create_%s_content_by_attrs' % key.split("_")[0]))
            self.page_type_config[key].append(getattr(self, '_create_%s_content_by_text' % key.split("_")[0]))

        self.is_text = False  # 是否为原始文本页面
        # 页面类型
        self.page_types = {
            "1": "api",
            "2": "schema_input",
            "3": "schema_output",
            "4": "idl",
            "5": "schema_object",
            "6": "model",
            "7": "request"
        }

        self.value = StringVar()
        self.value.set("1")
        for mode, text in self.page_types.items():
            Radiobutton(
                root, text=text, variable=self.value, value=mode, command=self.trigger_select).grid(
                row=int(mode), column=0, sticky=W)

    def trigger_select(self):
        print self.page_types.get(self.value.get())
        if self.is_text:
            self._change_text_interface()
        else:
            self._change_attrs_interface()

    def get_types(self):
        return self.page_type_config.get(self.page_types.get(self.value.get()))

    def _change_attrs_interface(self):
        pass

    def _change_text_interface(self):
        pass

    # def _create_api_content_by_attrs(self):
    #     pass

    # def _create_schema_content_by_attrs(self):
    #     pass

    def _create_idl_content_by_attrs(self):
        pass

    def _create_model_content_by_attrs(self):
        pass

    def _create_request_content_by_attrs(self):
        pass

    # def _create_api_content_by_text(self):
    #     pass

    # def _create_schema_content_by_text(self):
    #     pass

    def _create_idl_content_by_text(self):
        pass

    def _create_model_content_by_text(self):
        pass

    def _create_request_content_by_text(self):
        pass
