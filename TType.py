#!/usr/bin/env python
# -*- coding:utf-8 -*-
from enum import Enum


RealAPIType = ["number",
               "string",
               "boolean",
               "array",
               "Timestamp"]

APITypes = ["number_int",
            "number_double",
            "string",
            "boolean",
            "array",
            "Timestamp"]

SchemaTypes = ["Int",
               "Decimal",
               "Str",
               "Bool",
               "List",
               "Arrow",
               "Float"]

IdlTypes = ["i32",
            "double",
            "string",
            "bool",
            "list",
            "i64"]

ModelTypes = ["Integer",
              "Numeric",
              "String",
              "Boolean",
              "ScalarListType",
              "ArrowType"]


class APITType(Enum):
    number_int = 0
    number_double = 1
    string = 2
    boolean = 3
    array = 4
    Timestamp = 5


class SchemaTType(Enum):
    Int = 0
    Decimal = 1
    Str = 2
    Bool = 3
    List = 4
    Arrow = 5
    Float = 6


class IdlTType(Enum):
    i32 = 0
    double = 1
    string = 2
    bool = 3
    list = 4
    i64 = 5


class ModelTType(Enum):
    Integer = 0
    Numeric = 1
    String = 2
    Boolean = 3
    ScalarListType = 4
    ArrowType = 5
