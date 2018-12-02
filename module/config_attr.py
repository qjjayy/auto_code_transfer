#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from ttk import Combobox
from TType import *
from page_type import PageConfig
from collections import OrderedDict


class AttributeConfig(PageConfig):
    """
        页面属性栏配置
    """

    def __init__(self, root):
        super(AttributeConfig, self).__init__(root)
        # 创建属性栏
        self.group = LabelFrame(root, text="Attributes", padx=5, pady=5)
        self.group.grid(row=1, column=2, rowspan=100)
        Button(self.group, text="add_attr", command=self.add_attr).grid(row=101, column=0)
        Button(self.group, text="remove_attr", command=self.remove_attr).grid(row=101, column=2)
        Button(self.group, text="remove_all", command=self.remove_all).grid(row=101, column=5)
        # 配置参数的页面属性
        self.properties = OrderedDict([
            ('name', {'width': 15}),
            ('required', {'width': 5, 'type': ['True', 'False']}),
            ('doc', {'width': 10}),
            ('value', {'width': 20}),
            ('type', {'width': 10, 'type': APITypes}),
            ('inner_type', {'width': 10, 'type': APITypes}),
            ('nest_type', {'width': 10}),
            ('inner_nest_type', {'width': 10})
        ])
        # 类型切换按钮（列表筛选框和输入框（输入自定义类型）之间的切换）
        Button(self.group, text='type', command=self.change_type).grid(row=0, column=4)
        self.inner_type_button = Button(
            self.group, text='inner_type', command=self.change_inner_type, state=DISABLED)
        self.inner_type_button.grid(row=0, column=5)
        # 初始化输入框
        self.attr_count = 1
        for i, property_name in enumerate(self.properties.keys()):
            configs = self.properties.get(property_name)
            if i < len(self.properties.keys()) - 4:
                Label(self.group, text=property_name, width=configs.get('width')).grid(row=0, column=i)
            setattr(self, 'attr_%ss' % property_name, [StringVar()])  # 存储各页面对应的输入值
            setattr(self, 'entry_%ss' % property_name, list())        # 存储各页面对应的输入框
            if 'type' not in configs:  # Entry
                getattr(self, 'entry_%ss' % property_name).append(
                    Entry(self.group,
                          width=configs.get('width'),
                          textvariable=getattr(self, 'attr_%ss' % property_name)[0]))
            else:  # Combobox
                getattr(self, 'entry_%ss' % property_name).append(
                    Combobox(self.group,
                             width=configs.get('width'),
                             textvariable=getattr(self, 'attr_%ss' % property_name)[0],
                             values=configs.get('type')))
                getattr(self, 'entry_%ss' % property_name)[0].current(0)
            if self.__is_column_show(i):
                getattr(self, 'entry_%ss' % property_name)[0].grid(row=1, column=i)
        # Combobox（类型筛选）
        getattr(self, 'entry_types')[0].bind('<<ComboboxSelected>>', self.on_select)
        getattr(self, 'entry_inner_types')[0].bind('<<ComboboxSelected>>', self.on_select_inner)
        getattr(self, 'entry_inner_types')[0]['state'] = DISABLED

    @property
    def type_column(self):
        return 4

    @property
    def inner_type_column(self):
        return 5

    # ############################# 按钮触发动作 #############################

    def add_attr(self):
        """添加一行数据"""
        for i, property_name in enumerate(self.properties.keys()):
            configs = self.properties.get(property_name)
            getattr(self, 'attr_%ss' % property_name).append(StringVar())
            if 'type' not in configs:
                getattr(self, 'entry_%ss' % property_name).append(
                    Entry(self.group, width=configs.get('width'),
                          textvariable=getattr(self, 'attr_%ss' % property_name)[self.attr_count]))
            else:
                getattr(self, 'entry_%ss' % property_name).append(
                    Combobox(self.group, width=configs.get('width'),
                             textvariable=getattr(self, 'attr_%ss' % property_name)[self.attr_count],
                             values=configs.get('type')))
                getattr(self, 'entry_%ss' % property_name)[self.attr_count].current(0)
            if self.__is_column_show(i):
                getattr(self, 'entry_%ss' % property_name)[self.attr_count].grid(row=self.attr_count + 1, column=i)

        getattr(self, 'entry_types')[self.attr_count].bind('<<ComboboxSelected>>', self.on_select)
        getattr(self, 'entry_inner_types')[self.attr_count].bind('<<ComboboxSelected>>', self.on_select_inner)
        getattr(self, 'entry_inner_types')[self.attr_count]['state'] = DISABLED
        self.attr_count += 1

    def remove_attr(self):
        """删除当前数据行"""
        if self.attr_count == 0:
            return
        widget = self.group.focus_get()
        if hasattr(widget, 'grid_info'):
            remove_row = widget.grid_info()['row']
        else:
            remove_row = 0
        self.__remove_attr_by_cursor(int(remove_row) - 1)

    def remove_all(self):
        """删除所有数据行"""
        count = self.attr_count
        for i in range(count):
            getattr(self, 'entry_types')[self.attr_count - 1].focus_force()
            self.remove_attr()

    def on_select(self, event):
        """数据类型选择触发动作（是否显示嵌套数据类型）"""
        widget = event.widget
        row = getattr(self, 'entry_types').index(widget)
        if widget.current() == 4:  # type == list, inner_type is normal
            getattr(self, 'entry_inner_types')[row]['state'] = NORMAL
            self.inner_type_button['state'] = NORMAL
        else:
            self.__reset_entry_inner_type(row)

    def on_select_inner(self, event):
        """嵌套数据类型选择触发动作(TODO)"""
        widget = event.widget
        row = getattr(self, 'entry_inner_types').index(widget)
        pass

    def change_type(self):
        """输入框和筛选框切换（数据类型）"""
        self.__change_type(4)

    def change_inner_type(self):
        """输入框和筛选框切换（嵌套数据类型）"""
        self.__change_type(5, change_name='inner_')

    def _change_attrs_interface(self):
        """切换属性栏页面"""
        super(AttributeConfig, self)._change_attrs_interface()
        self.properties['type']['type'] = self.current_data_type
        self.properties['inner_type']['type'] = self.current_data_type
        map(self.__modify_attrs_type, getattr(self, 'entry_types'))
        map(self.__modify_attrs_type, getattr(self, 'entry_inner_types'))
        if self.prev_page_name == 'idl':
            self.idl_nested_source = dict()
            map(self.__truncate_idl_nested_types, getattr(self, 'attr_nest_types'))
            map(self.__truncate_idl_nested_types, getattr(self, 'attr_inner_nest_types'))
        elif self.current_page_name == 'idl':
            map(self.__recover_idl_nested_types, getattr(self, 'attr_nest_types'))
            map(self.__recover_idl_nested_types, getattr(self, 'attr_inner_nest_types'))

    def __is_column_show(self, column):
        """统一配置当前列是否能够显示"""
        if column < len(self.properties.keys()) - 2:  # nest_type初始化状态不显示
            return True
        else:
            return False

    def __remove_attr_by_cursor(self, row):
        """根据光标删除当前数据行"""
        for property_name in self.properties.keys():
            getattr(self, 'attr_%ss' % property_name).pop(row)
            getattr(self, 'entry_%ss' % property_name).pop(row).grid_forget()
        self.__reset_grid_locations()
        self.attr_count -= 1

    def __reset_grid_locations(self):
        """重新设置剩下的数据行"""
        for column, property_name in enumerate(self.properties.keys()):
            if self.__is_column_show(column):
                widgets = getattr(self, 'entry_%ss' % property_name)
                for row, widget in enumerate(widgets):
                    widget.grid(row=row + 1, column=column)

    def __reset_entry_inner_type(self, row):
        """inner_type对应的输入框恢复默认值"""
        self.inner_type_button['state'] = DISABLED
        getattr(self, 'attr_inner_nest_types')[row].set('')
        getattr(self, 'entry_inner_nest_types')[row].grid_remove()
        getattr(self, 'entry_inner_types')[row].grid(row=row + 1, column=5)
        getattr(self, 'entry_inner_types')[row]['state'] = DISABLED
        getattr(self, 'entry_inner_types')[row].current(0)

    def __change_type(self, change_column, change_name=''):
        """在输入框和筛选框之间切换"""
        widget = self.group.focus_get()
        if not hasattr(widget, 'grid_info'):
            return
        change_row = int(widget.grid_info()['row']) - 1

        if isinstance(widget, Combobox):
            if change_column == 4:  # 单类型
                getattr(self, 'entry_types')[change_row].current(0)
                self.__reset_entry_inner_type(change_row)
            else:  # 列表类型
                getattr(self, 'entry_inner_types')[change_row].current(0)  # TODO 可以去除？
            getattr(self, 'entry_%stypes' % change_name)[change_row].grid_remove()
            getattr(self, 'entry_%snest_types' % change_name)[change_row].grid(
                row=change_row + 1, column=change_column)
        else:
            getattr(self, 'attr_%snest_types' % change_name)[change_row].set('')
            getattr(self, 'entry_%snest_types' % change_name)[change_row].grid_remove()
            getattr(self, 'entry_%stypes' % change_name)[change_row].grid(
                row=change_row + 1, column=change_column)

    def __modify_attrs_type(self, widget):
        """重置页面参数类型"""
        if isinstance(widget, Combobox):
            type_index = widget.current()
            widget['values'] = self.current_data_type
            widget.current(type_index)

    def __truncate_idl_nested_types(self, attr_value):
        """处理Idl源文件的对应关系"""
        value = attr_value.get()
        values = value.split('.')
        if len(values) == 2:
            source = values[0]
            nested_value = values[1]
            attr_value.set(nested_value)
            self.idl_nested_source[nested_value] = source

    def __recover_idl_nested_types(self, attr_value):
        """恢复Idl源文件"""
        value = attr_value.get()
        if value in self.idl_nested_source:
            idl_value = self.idl_nested_source[value] + '.' + value
            attr_value.set(idl_value)

    def change_menu(self):
        """特殊处理"""
        pass
        # map(self.__truncate_idl_nested_types, getattr(self, 'attr_nest_types'))
        # map(self.__truncate_idl_nested_types, getattr(self, 'attr_inner_nest_types'))

if __name__ == '__main__':
    root = Tk()
    app = AttributeConfig(root)
    root.mainloop()
    root.destroy()
