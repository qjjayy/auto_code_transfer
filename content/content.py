#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .api_content import APIContent
from .schema_content import SchemaContent


class Content(APIContent, SchemaContent):
    pass
