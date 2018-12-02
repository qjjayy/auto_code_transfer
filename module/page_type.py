#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from TType import *
from content import *
from collections import OrderedDict


class PageConfig(APIContent, IdlContent, ModelContent, SchemaContent):
    """
        页面的基本配置
    """

    def __init__(self, root):
        self.is_text = False  # 是否为原始文本页面
        # 设置页面基本属性
        self.pages_config = OrderedDict([
            ("api", {'type': APITypes}),
            ("schema", {'type': SchemaTypes}),
            ("idl", {'type': IdlTypes}),
            ("model", {'type': ModelTypes}),
            ("request", {'type': None})
        ])
        # 设置页面对应的构建数据方法
        for key, value in self.pages_config.items():
            self.pages_config[key]['create_by_attr'] = getattr(
                self, '_create_%s_content_by_attrs' % key)
            self.pages_config[key]['create_by_text'] = getattr(
                self, '_create_%s_content_by_text' % key)
        # 设置页面类型
        self.page_types = dict()
        for i, key in enumerate(self.pages_config.keys()):
            self.page_types[str(i + 1)] = key
        # 绘制页面Radio选项
        self.value = StringVar()
        self.value.set("1")
        for mode, text in self.page_types.items():
            Radiobutton(
                root, text=text, variable=self.value, value=mode,
                command=self.trigger_select).grid(
                row=int(mode), column=0, sticky=W)

        self.__special_init()

    def __special_init(self):
        self.his_values = [self.value.get()]  # 获取原始页面的特殊手段
        self.idl_nested_source = dict()

    @property
    def current_page_index(self):
        return self.value.get()

    @property
    def prev_page_index(self):
        return self.his_values[0]

    @property
    def current_page_name(self):
        return self.page_types.get(self.current_page_index)

    @property
    def prev_page_name(self):
        return self.page_types.get(self.prev_page_index)

    @property
    def current_page_config(self):
        return self.pages_config.get(self.current_page_name)

    @property
    def current_data_type(self):
        return self.current_page_config.get('type')

    @property
    def create_by_attr_func(self):
        return self.current_page_config.get('create_by_attr')

    @property
    def create_by_text_func(self):
        return self.current_page_config.get('create_by_text')

    def trigger_select(self):
        """Radio选项触发动作"""
        print self.page_types.get(self.value.get())
        self.his_values.append(self.value.get())
        if len(self.his_values) == 3:
            self.his_values.pop(0)

        if self.is_text:
            self._change_text_interface()
        else:
            self._change_attrs_interface()

    def _change_attrs_interface(self):
        """切换属性栏页面"""
        pass

    def _change_text_interface(self):
        """切换文本内容页面"""
        pass

    # def _create_api_content_by_attrs(self):
    #     pass

    # def _create_schema_content_by_attrs(self):
    #     pass

    # def _create_idl_content_by_attrs(self):
    #     pass

    # def _create_model_content_by_attrs(self):
    #     pass

    def _create_request_content_by_attrs(self):
        pass

    # def _create_api_content_by_text(self):
    #     pass

    # def _create_schema_content_by_text(self):
    #     pass

    # def _create_idl_content_by_text(self):
    #     pass
    #
    # def _create_model_content_by_text(self):
    #     pass

    def _create_request_content_by_text(self):
        pass
