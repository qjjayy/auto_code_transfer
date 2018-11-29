#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from ttk import Combobox
from TType import *
from format import format_request
from module import AttributeConfig
from content import Content
TAP = "    "


class App(AttributeConfig, Content):
    def __init__(self, root):
        super(App, self).__init__(root)
        # request内容格式转换
        self.request_format = Button(root, text="format", command=self.format_request_content, state=DISABLED)
        self.request_format.grid(row=8, column=0)

        self.text_area = Text(root, height=100, width=150, borderwidth=2, relief="solid", font="Menlo")

        Button(root, text="退出", command=root.quit).grid(row=0, column=0)
        Button(root, text="生成当前内容", command=self.create_local_content).grid(row=0, column=1)
        Button(root, text="生成全局内容", command=self.create_global_content).grid(row=0, column=3)
        self.content_button = Button(root, text="切换至文本内容页面", command=self.change_menu)
        self.content_button.grid(row=0, column=2)
        # 文本内容
        self.content_show = None
        self.content_map = dict()
        for name in self.page_type_config.keys():
            self.content_map[name] = list()

    @property
    def page_name(self):
        return self.page_types.get(self.value.get())

    def format_request_content(self):
        formatted_request = format_request(self.text_area.get(1.0, END))
        self.text_area.delete(1.0, END)
        self.text_area.insert(END, formatted_request)

    def change_menu(self):
        if not self.is_text:
            self.is_text = True
            self.group.grid_remove()
            self.text_area.grid(row=1, column=2, rowspan=100)
            self.content_button['text'] = "切换至属性栏页面"
            self.__flush_content()
        else:
            self.is_text = False
            self.text_area.grid_remove()
            self.group.grid(row=1, column=2, rowspan=100)
            self.content_button['text'] = "切换至文本内容页面"

    def _change_text_interface(self):
        super(App, self)._change_text_interface()
        self.content_show = self.content_map[self.page_name]
        self.__flush_content()
        if self.page_types.get(self.value.get()) == "request":
            self.request_format['state'] = NORMAL
        else:
            self.request_format['state'] = DISABLED

    def __flush_content(self):
        self.text_area.delete(1.0, END)
        if self.content_show:
            for i in range(len(self.content_show)):
                self.text_area.insert(END, self.content_show[i])

    def create_local_content(self):
        if not self.is_text:
            self._create_local_content_by_attrs()
        else:
            self._create_local_content_by_text()

    def _create_local_content_by_attrs(self):
        type_conf = self.get_types()
        self.content_map[self.page_name] = type_conf[3]()
        self.content_show = self.content_map[self.page_name]

    def _create_local_content_by_text(self):
        self.remove_all()
        print self.get_types()[4]
        self.get_types()[4]()

    def create_global_content(self):
        current_index = self.value.get()
        for page_index in self.page_types.keys():
            self.value.set(page_index)
            self.trigger_select()
            self.create_local_content()
        self.value.set(current_index)
        self.trigger_select()
        self.content_show = self.content_map[self.page_name]

    # def __create_idl_content(self):
    #     content_list = list()
    #     for i in range(self.attr_count):
    #         if self.attr_bools[i].get():
    #             required = "required"
    #         else:
    #             required = "optional"
    #
    #         if self.attr_types[i].get() == "list":
    #             content_list.append(TAP + str(i + 1) + ": " + required + " list<" +
    #                                 self.attr_inner_types[i].get() + "> " + self.attr_names[i].get() + ",")
    #         else:
    #             content_list.append(TAP + str(i + 1) + ": " + required + " " +
    #                                 self.attr_types[i].get() + " " + self.attr_names[i].get() + ",")
    #     return content_list
    #
    # def __create_model_content(self):
    #     content_list = list()
    #     for i in range(self.attr_count):
    #         content_str = TAP + self.attr_names[i].get() + " = Column(\n" + TAP + TAP + \
    #                       self.__get_model_specific_attr_type(self.attr_types[i].get()) + \
    #                       ", doc=u'" + self.attr_docs[i].get() + "', nullable=False"
    #         if self.attr_bools[i].get():
    #             content_str += ")\n"
    #         else:
    #             content_str += ", default=" + self.__get_model_missing(self.attr_types[i].get()) + ")\n"
    #         content_list.append(content_str)
    #     return content_list
    #
    # def __get_model_specific_attr_type(self, attr_type):
    #     if attr_type == "String":
    #         return "String(255)"
    #     elif attr_type == "Numeric":
    #         return "Numeric(precision=11, scale=3)"
    #     elif attr_type == "ScalarListType":
    #         return "ScalarListType(unicode)"
    #     elif attr_type == "ArrowType":
    #         return "ArrowType()"
    #     else:
    #         return attr_type
    #
    # def __get_model_missing(self, attr_type):
    #     if attr_type == "String":
    #         return "u''"
    #     elif attr_type == "Boolean":
    #         return "False"
    #     elif attr_type == "ScalarListType":
    #         return "[]"
    #     else:
    #         return "0"


if __name__ == '__main__':
    root = Tk()
    root.title("helper")
    app = App(root)
    root.mainloop()
    root.destroy()
