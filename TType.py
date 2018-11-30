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
               "Float",
               "Str",
               "Bool",
               "List",
               "Arrow",
               "Decimal"]

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
    number_int = "number_int"
    number_double = "number_double"
    string = "string"
    boolean = "boolean"
    array = "array"
    Timestamp = "Timestamp"


class SchemaTType(Enum):
    Int = "Int"
    Float = "Float"
    Str = "Str"
    Bool = "Bool"
    List = "List"
    Arrow = "Arrow"
    Decimal = "Decimal"


class IdlTType(Enum):
    i32 = "i32"
    double = "double"
    string = "string"
    bool = "bool"
    list = "list"
    i64 = "i64"


class ModelTType(Enum):
    Integer = "Integer"
    Numeric = "Numeric"
    String = "String"
    Boolean = "Boolean"
    ScalarListType = "ScalarListType"
    ArrowType = "ArrowType"
