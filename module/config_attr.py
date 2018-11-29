#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from ttk import Combobox
from TType import *
from page_type import PageConfig
from collections import OrderedDict


class AttributeConfig(PageConfig):

    def __init__(self, root):
        super(AttributeConfig, self).__init__(root)
        # 创建属性栏
        self.group = LabelFrame(root, text="Attribute_Group", padx=5, pady=5)
        self.group.grid(row=1, column=2, rowspan=100)
        Button(self.group, text="add_attr", command=self.add_attr).grid(row=101, column=0)
        Button(self.group, text="remove_attr", command=self.remove_attr).grid(row=101, column=2)
        Button(self.group, text="remove_all", command=self.remove_all).grid(row=101, column=5)

        self.properties = OrderedDict([
            ('name', [15]),
            ('required', [5, ['True', 'False']]),
            ('doc', [10]),
            ('value', [20]),
            ('type', [10, APITypes]),
            ('inner_type', [10, APITypes]),
            ('nest_type', [10]),
            ('inner_nest_type', [10])
        ])

        Button(self.group, text='type', command=self.change_type).grid(row=0, column=4)
        self.inner_type_button = Button(
            self.group, text='inner_type', command=self.change_inner_type, state=DISABLED)
        self.inner_type_button.grid(row=0, column=5)

        self.attr_count = 1
        for i, property_name in enumerate(self.properties.keys()):
            configs = self.properties.get(property_name)
            if i < len(self.properties.keys()) - 4:
                Label(self.group, text=property_name, width=configs[0]).grid(row=0, column=i)
            setattr(self, 'attr_%ss' % property_name, [StringVar()])
            setattr(self, 'entry_%ss' % property_name, list())
            if len(configs) == 1:  # Entry
                getattr(self, 'entry_%ss' % property_name).append(
                    Entry(self.group, width=configs[0], textvariable=getattr(self, 'attr_%ss' % property_name)[0]))
            else:  # Combobox
                getattr(self, 'entry_%ss' % property_name).append(
                    Combobox(self.group, width=configs[0], textvariable=getattr(self, 'attr_%ss' % property_name)[0],
                             values=configs[1]))
                getattr(self, 'entry_%ss' % property_name)[0].current(0)
            if self.__is_column_show(i):
                getattr(self, 'entry_%ss' % property_name)[0].grid(row=1, column=i)

        getattr(self, 'entry_types')[0].bind('<<ComboboxSelected>>', self.on_select)
        getattr(self, 'entry_inner_types')[0].bind('<<ComboboxSelected>>', self.on_select_inner)
        getattr(self, 'entry_inner_types')[0]['state'] = DISABLED

    @property
    def type_column(self):
        return 4

    @property
    def inner_type_column(self):
        return 5

    def add_attr(self):
        for i, property_name in enumerate(self.properties.keys()):
            configs = self.properties.get(property_name)
            getattr(self, 'attr_%ss' % property_name).append(StringVar())
            if len(configs) == 1:
                getattr(self, 'entry_%ss' % property_name).append(
                    Entry(self.group, width=configs[0],
                          textvariable=getattr(self, 'attr_%ss' % property_name)[self.attr_count]))
            else:
                getattr(self, 'entry_%ss' % property_name).append(
                    Combobox(self.group, width=configs[0],
                             textvariable=getattr(self, 'attr_%ss' % property_name)[self.attr_count],
                             values=configs[1]))
                getattr(self, 'entry_%ss' % property_name)[self.attr_count].current(0)
            if self.__is_column_show(i):
                getattr(self, 'entry_%ss' % property_name)[self.attr_count].grid(row=self.attr_count + 1, column=i)

        getattr(self, 'entry_types')[self.attr_count].bind('<<ComboboxSelected>>', self.on_select)
        getattr(self, 'entry_inner_types')[self.attr_count].bind('<<ComboboxSelected>>', self.on_select_inner)
        getattr(self, 'entry_inner_types')[self.attr_count]['state'] = DISABLED
        self.attr_count += 1

    def remove_attr(self):
        if self.attr_count == 0:
            return
        widget = self.group.focus_get()
        if hasattr(widget, 'grid_info'):
            remove_row = widget.grid_info()['row']
        else:
            remove_row = 0
        self.__remove_attr_by_cursor(int(remove_row) - 1)

    def __remove_attr_by_cursor(self, row):
        for property_name in self.properties.keys():
            getattr(self, 'attr_%ss' % property_name).pop(row)
            getattr(self, 'entry_%ss' % property_name).pop(row).grid_forget()
        self.__reset_grid_locations()
        self.__remove_special_records(row)
        self.attr_count -= 1

    def __reset_grid_locations(self):
        for column, property_name in enumerate(self.properties.keys()):
            if self.__is_column_show(column):
                widgets = getattr(self, 'entry_%ss' % property_name)
                for row, widget in enumerate(widgets):
                    widget.grid(row=row + 1, column=column)

    def remove_all(self):
        count = self.attr_count
        for i in range(count):
            getattr(self, 'entry_types')[self.attr_count - 1].focus_force()
            self.remove_attr()

    def on_select(self, event):
        widget = event.widget
        row = getattr(self, 'entry_types').index(widget)
        if widget.current() == 4:  # type == list, inner_type is normal
            getattr(self, 'entry_inner_types')[row]['state'] = NORMAL
            self.inner_type_button['state'] = NORMAL
        else:
            self.__reset_entry_inner_type(row)
        self.__record_special(widget, row, index=1)

    def on_select_inner(self, event):
        widget = event.widget
        row = getattr(self, 'entry_inner_types').index(widget)
        self.__record_special(widget, row, index=2)

    def change_type(self):
        self.__change_type(4)

    def change_inner_type(self):
        self.__change_type(5, change_name='inner_')

    def _change_attrs_interface(self):
        super(AttributeConfig, self)._change_attrs_interface()
        self.properties['type'][1] = self.get_types()[0]
        self.properties['inner_type'][1] = self.get_types()[0]
        map(self.__modify_attrs_frame, getattr(self, 'entry_types'))
        map(self.__modify_attrs_frame, getattr(self, 'entry_inner_types'))

    def __change_type(self, change_column, change_name=''):
        widget = self.group.focus_get()
        if not hasattr(widget, 'grid_info'):
            return
        change_row = int(widget.grid_info()['row']) - 1

        if isinstance(widget, Combobox):
            if change_column == 4:  # 单类型
                getattr(self, 'entry_types')[change_row].current(0)
                self.__reset_entry_inner_type(change_row)
            else:  # 列表类型
                getattr(self, 'entry_inner_types')[change_row].current(0)
            self.__remove_special_records(change_row)
            getattr(self, 'entry_%stypes' % change_name)[change_row].grid_remove()
            getattr(self, 'entry_%snest_types' % change_name)[change_row].grid(row=change_row + 1, column=change_column)
        else:
            getattr(self, 'attr_%snest_types' % change_name)[change_row].set('')
            getattr(self, 'entry_%snest_types' % change_name)[change_row].grid_remove()
            getattr(self, 'entry_%stypes' % change_name)[change_row].grid(row=change_row + 1, column=change_column)

    def __reset_entry_inner_type(self, row):
        """重置inner_type对应的输入框"""
        self.inner_type_button['state'] = DISABLED
        getattr(self, 'attr_inner_nest_types')[row].set('')
        getattr(self, 'entry_inner_nest_types')[row].grid_remove()
        getattr(self, 'entry_inner_types')[row].grid(row=row + 1, column=5)
        getattr(self, 'entry_inner_types')[row]['state'] = DISABLED
        getattr(self, 'entry_inner_types')[row].current(0)

    def __modify_attrs_frame(self, widget):
        if isinstance(widget, Combobox):
            type_index = self.__get_index(widget)
            widget['values'] = self.get_types()[0]
            widget.current(type_index)

    def __get_index(self, widget):
        """正确获取类型索引"""
        if 'column' not in widget.grid_info():  # 针对转换成了nest_type的情况
            return 0
        if widget.grid_info()['column'] == str(4):  # types 获取Schema特殊记录
            row = getattr(self, 'entry_types').index(widget)
            index = 1
        else:  # inner_types 获取Schema特殊记录
            row = getattr(self, 'entry_inner_types').index(widget)
            index = 2
        if not self.get_types()[index] and widget.get() == "Float":  # 非Schema正确转换
            return 1
        elif self.get_types()[index]:  # Schema正确转换
            if row in self.get_types()[index]:
                return 6
            elif widget.get() == "Float":
                return 1
            else:
                return widget.current()
        else:
            return widget.current()

    def __record_special(self, widget, row, index):
        """
            记录Schema中类型为Float的属性，因为Json不认Decimal类型
            index 标示 哪一个Float列表
        """
        if widget.get() == "Float" and row not in self.get_types()[index]:
            self.get_types()[index].append(row)
        elif self.get_types()[index] and row in self.get_types()[index]:
            self.get_types()[index].remove(row)
        elif not self.get_types()[index]:
            self.__remove_special_records(row, index)

    def __remove_special_records(self, row, index=-1):
        """清除当前行的所有Float记录"""
        names = ['input', 'output', 'object']
        if index == -1 or index == 1:
            for name in names:
                if row in getattr(self, '%s_float' % name):
                    getattr(self, '%s_float' % name).remove(row)
        if index == -1 or index == 2:
            for name in names:
                if row in getattr(self, 'inner_%s_float' % name):
                    getattr(self, 'inner_%s_float' % name).remove(row)
                
    def __is_column_show(self, column):
        """统一配置当前列是否能够显示"""
        if column < len(self.properties.keys()) - 2:  # nest_type初始化状态不显示
            return True
        else:
            return False


if __name__ == '__main__':
    root = Tk()
    app = AttributeConfig(root)
    root.mainloop()
    root.destroy()
