#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .content import Content, TAP
from faker_tool import faker_tool


class RequestContent(Content):
    """
        Request文档数据的构建
    """

    def _create_request_content_by_attrs(self):
        content_list = list()
        for i in range(getattr(self, 'attr_count')):
            attribute = self._get_attribute(i)

            current_data_type = getattr(self, 'current_data_type')
            if attribute.type_name in current_data_type:
                type_index = current_data_type.index(attribute.type_name)
            else:
                type_index = None
            if attribute.inner_type_name in current_data_type:
                inner_type_index = current_data_type.index(attribute.inner_type_name)
            else:
                inner_type_index = None
            fake_value = faker_tool.get_optimum_fake_value(attribute.name, type_index, inner_type_index)

            if isinstance(fake_value, list):
                value = '[\n'
                for item in fake_value:
                    value += TAP + TAP + str(item) + '\n'
                value += TAP + ']'
            else:
                value = str(fake_value)
            content_line = TAP + '\'' + attribute.name + '\': ' + value + '\n'
            content_list.append(content_line)

        return content_list
