#!/usr/bin/env python
# -*- coding:utf-8 -*-
from enum import Enum


class APITType(Enum):
    REAL_INTEGER = 'number'
    INTEGER = "number_int"
    DOUBLE = "number_double"
    STRING = "string"
    BOOLEAN = "boolean"
    LIST = "array"
    TIMESTAMP = "Timestamp"


class SchemaTType(Enum):
    INTEGER = "Int"
    DOUBLE = "Float"
    STRING = "Str"
    BOOLEAN = "Bool"
    LIST = "List"
    TIMESTAMP = "Arrow"
    DECIMAL = "Decimal"


class IdlTType(Enum):
    INTEGER = "i32"
    DOUBLE = "double"
    STRING = "string"
    BOOLEAN = "bool"
    LIST = "list"
    TIMESTAMP = "i64"


class ModelTType(Enum):
    INTEGER = "Integer"
    DOUBLE = "Numeric"
    STRING = "String"
    BOOLEAN = "Boolean"
    LIST = "ScalarListType"
    TIMESTAMP = "ArrowType"
    CHOICE_TYPE = "ChoiceType"


RealAPITypes = [
    APITType.REAL_INTEGER,
    APITType.STRING,
    APITType.BOOLEAN,
    APITType.LIST,
    APITType.TIMESTAMP,
]

RealIdlTypes = [
    IdlTType.INTEGER,
    IdlTType.DOUBLE,
    IdlTType.STRING,
    IdlTType.BOOLEAN,
    IdlTType.LIST,
    IdlTType.TIMESTAMP,
]

# 数据类型的映射配置

APITypes = [
    APITType.INTEGER,
    APITType.DOUBLE,
    APITType.STRING,
    APITType.BOOLEAN,
    APITType.LIST,
    APITType.TIMESTAMP,
    APITType.DOUBLE,
    APITType.STRING,
]

SchemaTypes = [
    SchemaTType.INTEGER,
    SchemaTType.DOUBLE,
    SchemaTType.STRING,
    SchemaTType.BOOLEAN,
    SchemaTType.LIST,
    SchemaTType.TIMESTAMP,
    SchemaTType.DECIMAL,
    SchemaTType.STRING,
]

IdlTypes = [
    IdlTType.INTEGER,
    IdlTType.DOUBLE,
    IdlTType.STRING,
    IdlTType.BOOLEAN,
    IdlTType.LIST,
    IdlTType.TIMESTAMP,
    IdlTType.DOUBLE,
    IdlTType.STRING,
]

ModelTypes = [
    ModelTType.INTEGER,
    ModelTType.DOUBLE,
    ModelTType.STRING,
    ModelTType.BOOLEAN,
    ModelTType.LIST,
    ModelTType.TIMESTAMP,
    ModelTType.DOUBLE,
    ModelTType.CHOICE_TYPE,
]
