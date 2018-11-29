#!/usr/bin/env python
# -*- coding:utf-8 -*-


class AttributeType(object):
    def __init__(self, name, inner_name):
        self.name = name
        self.inner_name = inner_name


class APIAttribute(object):
    def __init__(self, name, attr_type, required, doc, value):
        self.name = name
        self.attr_type = attr_type
        self.required = required
        self.doc = doc
        self.value = value


class SchemaAttribute(object):
    def __init__(self, name, attr_type, required):
        self.name = name
        self.attr_type = attr_type
        self.required = required


class IdlAttribute(object):
    def __init__(self, name, attr_type, required):
        self.name = name
        self.attr_type = attr_type
        self.required = required


class ModelAttribute(object):
    def __init__(self, name, attr_type, required, doc):
        self.name = name
        self.attr_type = attr_type
        self.required = required
        self.doc = doc


class RequestArgs(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
