#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tkinter import *
from module import AttributeConfig


class App(AttributeConfig):
    """
        代码转换工具1.0版
    """

    def __init__(self, root):
        super(App, self).__init__(root)
        # 原始文本框
        self.text_area = Text(root, height=100, width=150, borderwidth=2, relief="solid", font="Menlo")
        # 系统按钮
        Button(root, text="退出", command=root.quit).grid(row=0, column=0)
        Button(root, text="生成当前内容", command=self.create_local_content).grid(row=0, column=1)
        Button(root, text="生成全局内容", command=self.create_global_content).grid(row=0, column=3)
        self.content_button = Button(root, text="切换至文本内容页面", command=self.change_menu)
        self.content_button.grid(row=0, column=2)
        # 文本内容
        self.content_show = None
        self.content_map = dict()
        for name in self.pages_config.keys():
            self.content_map[name] = list()

    def create_local_content(self):
        """编辑当前页面的内容"""
        if not self.is_text:
            self.content_map[self.current_page_name] = self.create_by_attr_func()
            self.content_show = self.content_map[self.current_page_name]
        else:
            self.remove_all()
            self.create_by_text_func()

    def create_global_content(self):
        """编辑全部页面的内容"""
        current_index = self.current_page_index
        for page_index in self.page_types.keys():
            self.value.set(page_index)
            self.trigger_select()
            self.create_local_content()
        self.value.set(current_index)
        self.trigger_select()
        self.content_show = self.content_map[self.current_page_name]

    def change_menu(self):
        """在属性栏页面和文本页面之间切换"""
        super(App, self).change_menu()
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
        """切换文本内容页面"""
        super(App, self)._change_text_interface()
        self.content_show = self.content_map[self.current_page_name]
        self.__flush_content()

    def __flush_content(self):
        """刷新文本内容"""
        self.text_area.delete(1.0, END)
        if self.content_show:
            for i in range(len(self.content_show)):
                self.text_area.insert(END, self.content_show[i])


if __name__ == '__main__':
    root = Tk()
    root.title("helper")
    app = App(root)
    root.mainloop()
    root.destroy()
