#!/usr/bin/env python
# -*- coding:utf-8 -*-
TAP = "    "


# 对长string仍然有bug,但就这样了，手动修改吧
def format_request(request_content):
    item_list = list()
    for item in request_content:
        item_list.append(item)
    tap_deep = 1
    line_length = 0
    for i in range(len(item_list)):
        line_length += len(item_list[i])
        if line_length > 120:
            j = i
            while j > 0 and item_list[j] != ",":
                j -= 1
            add_return_after(item_list, j + 1, tap_deep - 1)
            line_length = (tap_deep - 1) * 4 + len(item_list[j + 1])

        if item_list[i] == "{":
            add_return_before(item_list, i + 1, tap_deep)
            line_length = tap_deep * 4 + len(item_list[i + 1])
            j = i - 1
            if j > 0:
                while item_list[j] != "{" and item_list[j] != ",":
                    j -= 1
                if item_list[j] == ",":
                    item_list[j + 1] = ""
                    add_return_before(item_list, j + 1, tap_deep - 1)
                    line_length = (tap_deep - 1) * 4 + len(item_list[j + 1])
            tap_deep += 1
        elif item_list[i] == "}":
            tap_deep -= 1
            add_return_after(item_list, i - 1, tap_deep - 1)
            line_length = (tap_deep - 1) * 4 + 1
            j = i + 1
            while j < len(item_list) and item_list[j] != "}" and item_list[j] != ",":
                j += 1
            if j < len(item_list) - 1:
                item_list[j + 1] = ""
                add_return_before(item_list, j + 1, tap_deep - 1)
                line_length = (tap_deep - 1) * 4

    return ''.join(item_list)


def add_return_after(item_list, j, tap_deep):
    item_list[j] += "\n"
    for i in range(tap_deep):
        item_list[j] += TAP


def add_return_before(item_list, j, tap_deep):
    for i in range(tap_deep):
        item_list[j] = TAP + item_list[j]
    item_list[j] = "\n" + item_list[j]
