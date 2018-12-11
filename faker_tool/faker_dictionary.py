#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import yaml
import time
from frame import ENV
from TType import RealIdlTypes, IdlTypes
from fuzzywuzzy import fuzz
from faker import Faker
from bson import ObjectId

faker_yaml = yaml.load(
    open(os.path.join(ENV['root'], 'data', 'faker.yaml')))


class FakerTool(object):

    def __init__(self):
        self.fake = Faker()
        self.list_value_count = 2  # 列表mock的数量
        for i, faker_type in enumerate(RealIdlTypes):
            setattr(self, '%s_fake_func_dict' % faker_type, dict())
            config = faker_yaml.get(i)
            for key, values in config.items():
                for value in values:
                    getattr(self, '%s_fake_func_dict' % faker_type)[value] = key

    def get_optimum_fake_value(self, name, type_index=None, inner_type_index=None):
        """获取最优mock值"""
        if type_index is None:
            return 'None'
        fake_func_dict = getattr(
            self, '%s_fake_func_dict' % IdlTypes[type_index])
        max_ratio = 0
        best_name = ''
        for key, value in fake_func_dict.items():
            if key == 'default':  # default 为默认值，不进行比较
                continue

            if 'id' in name:  # id 带有强制性
                max_ratio = 100
                best_name = 'id'
                break

            current_ratio = fuzz.WRatio(name, key)
            if current_ratio > max_ratio:
                max_ratio = current_ratio
                best_name = key
        if max_ratio < 60:  # 最好设置成可调式的
            best_name = 'default'
        func_name = fake_func_dict.get(best_name)
        special_value = self.__get_special_fake_value(
            name, func_name, inner_type_index)
        if special_value:
            return special_value
        else:
            return self.__get_normal_fake_value(func_name, type_index)

    def __get_special_fake_value(self, name, func_name, inner_type_index):
        """获取特殊mock值"""
        if func_name == 'pylist':
            temp_list = list()
            for i in range(self.list_value_count):
                temp_list.append(self.get_optimum_fake_value(name, inner_type_index))
            return temp_list
        elif func_name == 'object_id':
            return str(ObjectId())
        else:
            return None

    def __get_normal_fake_value(self, func_name, type_index):
        """设置fake参数，并且获取正常mock值"""
        kwargs = dict()
        if func_name == 'random_int':
            kwargs['min'] = 0
            kwargs['max'] = 10
        elif func_name == 'pyfloat':
            kwargs['left_digits'] = 2
            kwargs['right_digits'] = 3
            kwargs['positive'] = True
        elif func_name == 'date_time_this_month':
            kwargs['before_now'] = False
            kwargs['after_now'] = True
        elif func_name == 'pystr':
            kwargs['max_chars'] = 5

        value = getattr(self.fake, func_name)(**kwargs)

        if func_name == 'date_time_this_month':
            value = int(time.mktime(value.timetuple()))
        if type_index == 2:
            value = '\'' + str(value) + '\''

        return value


faker_tool = FakerTool()
