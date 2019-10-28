#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re
from json import JSONDecodeError


class Int(object):
    def __init__(self, comment="", required=True, default=None, min_value=None, max_value=None, allow_zero=None,
                 enum=None):
        """

        :param comment:
        :param required:bool  是否是必须参数
        :param default:int  参数的默认值
        :param min_value:int
        :param max_value:int
        :param allow_zero:bool
        :param enum:list
        """
        self.comment = comment
        self.required = required
        self.default = default
        self.min_value = min_value
        self.max_value = max_value
        self.allow_zero = allow_zero
        self.enum = enum

    def validate(self, value):
        if value is None:
            if self.required is False:
                value = 0
            if self.default is not None:
                value = self.default
            if value is None:
                return "{%s} 参数不存在" % self.comment, value
        if type(value) in (str, float):
            try:
                value = int(value)
            except:
                pass
        if type(value) is not int:
            return "{%s} 参数类型错误" % self.comment, value
        if self.min_value is not None and not self.min_value <= value:
            return "{%s} 参数小于最小值:%s" % (self.comment, self.min_value), value
        if self.max_value is not None and not self.max_value >= value:
            return "{%s} 参数大于最大值:%s" % (self.comment, self.max_value), value
        if self.allow_zero is False and value == 0:
            return "{%s} 参数不能为0" % self.comment, value
        if self.enum is not None and value not in self.enum:
            return "{%s} 参数枚举值不合法" % self.comment, value

        return "", value


class Float(object):
    def __init__(self, comment="", required=True, default=None, min_value=None, max_value=None, allow_zero=None,
                 ):
        """

        :param comment: str
        :param required: bool
        :param default: float
        :param min_value: number
        :param max_value:number
        :param allow_zero: bool
        """
        self.comment = comment
        self.required = required
        self.default = default
        self.min_value = min_value
        self.max_value = max_value
        self.allow_zero = allow_zero

    def validate(self, value):
        if value is None:
            if self.required is False:
                value = 0.0
            if self.default is not None:
                value = self.default
            if value is None:
                return "{%s} 参数不存在" % self.comment, value
        if type(value) in (int, str):
            try:
                value = float(value)
            except:
                pass

        if type(value) is not float:
            return "{%s} 参数类型错误" % self.comment, value
        if self.min_value is not None and not self.min_value <= value:
            return "{%s} 参数小于最小值:%s" % (self.comment, self.min_value), value
        if self.max_value is not None and not self.max_value >= value:
            return "{%s} 参数大于最大值:%s" % (self.comment, self.max_value), value
        if self.allow_zero is False and value == 0.0:
            return "{%s} 参数不能为0.0" % self.comment, value

        return "", value


class Str(object):
    def __init__(self, comment="", required=True, default=None, min_length=None, max_length=None, allow_empty=None,
                 pattern=None, enum=None,
                 ):
        """

        :param comment: str
        :param required: bool
        :param default: str
        :param min_length: int
        :param max_length: int
        :param allow_empty: bool
        :param pattern: str
        :param enum: list
        """
        self.comment = comment
        self.required = required
        self.default = default
        self.min_length = min_length
        self.max_length = max_length
        self.allow_empty = allow_empty
        self.pattern = pattern
        self.enum = enum

    def validate(self, value):
        if value is None:
            if self.required is False:
                value = ""
            if self.default is not None:
                value = self.default
            if value is None:
                return "{%s} 参数不存在" % self.comment, value
        if type(value) is not str:
            return "{%s} 参数类型错误" % self.comment, value
        if self.min_length is not None and not self.min_length <= len(value):
            return "{%s} 参数长度小于最小值:%s" % (self.comment, self.min_length), value
        if self.max_length is not None and not self.max_length >= len(value):
            return "{%s} 参数长度大于最大值:%s" % (self.comment, self.max_length), value
        if self.allow_empty is False and len(value) == 0:
            return "{%s} 参数不能为空" % self.comment, value
        if self.pattern is not None and re.compile(self.pattern).match(value):
            return "{%s} 参数不满足正则条件:%s" % (self.comment, self.pattern), value
        if self.enum is not None and value not in self.enum:
            return "{%s} 参数枚举值不合法" % self.comment, value

        return "", value


class Dict(object):
    def __init__(self, struct=None, comment="", required=True, min_length=None, max_length=None, allow_empty=None,
                 ):
        """

        :param struct: 字典
        :param comment: str
        :param required: bool
        :param min_length: int
        :param max_length: int
        :param allow_empty: bool
        """
        self.struct = struct
        self.comment = comment
        self.required = required
        self.min_length = min_length
        self.max_length = max_length
        self.allow_empty = allow_empty

    def validate(self, value):
        if value is None:
            if self.required is False:
                value = {}
            else:
                return "{%s} 参数不存在" % self.comment, value

        if type(value) is str:
            try:
                value = json.loads(value)
            except JSONDecodeError:
                pass

        if type(value) is not dict:
            return "{%s} 参数类型错误" % self.comment, value

        if self.min_length is not None and not self.min_length <= len(value):
            return "{%s} 参数长度小于最短长度:%s" % (self.comment, self.min_length), value

        if self.max_length is not None and not self.max_length >= len(value):
            return "{%s} 参数长度大于最长长度:%s" % (self.comment, self.min_length), value

        if self.allow_empty is False and len(value) == 0:
            return "{%s} 参数不允许为空" % self.comment, value
        if self.struct is not None:
            ret = {}
            for sub_key, sub_struct in self.struct.items():
                err, sub_value = sub_struct.validate(value.get(sub_key, None))
                if not err:
                    ret[sub_key] = sub_value
                else:
                    return err, value
            return "", ret
        return "", value


class List(object):
    def __init__(self, struct=None, comment="", required=True, min_length=None, max_length=None, allow_empty=None,
                 ):
        """

        :param struct: 长度为1的列表，元素为校验实例
        :param comment:str
        :param required: bool
        :param min_length:int
        :param max_length:int
        :param allow_empty:bool
        """
        self.struct = struct
        self.comment = comment
        self.required = required
        self.min_length = min_length
        self.max_length = max_length
        self.allow_empty = allow_empty

    def validate(self, value):
        if value is None:
            if self.required is False:
                value = []
            else:
                return "{%s} 参数不存在" % self.comment, value

        if type(value) is str:
            try:
                value = json.loads(value)
            except JSONDecodeError:
                pass

        if type(value) is not list:
            return "{%s} 参数类型错误" % self.comment, value

        if self.min_length is not None and not self.min_length <= len(value):
            return "{%s} 参数长度小于最短长度:%s" % (self.comment, self.min_length), value

        if self.max_length is not None and not self.max_length >= len(value):
            return "{%s} 参数长度大于最长长度:%s" % (self.comment, self.min_length), value

        if self.allow_empty is False and len(value) == 0:
            return "{%s} 参数不允许为空" % self.comment, value
        if self.struct is not None:
            ret = []
            for sub_value in value:
                err, sub_value = self.struct[0].validate(sub_value)
                if not err:
                    ret.append(sub_value)
                else:
                    return err, value
            return "", ret

        return "", value


if __name__ == "__main__":
    value = {
        "user_id": 123,
        "tenant_id": 345,
        "question_list": [{
            "question_id": "asdfsdf",
            "question": "你好？",
            "answer": "我很好，你是谁？",
            "status": 0,
        }]
    }
    schema = Dict({
        "user_id": Int(comment="用户id"),
        "tenant_id": Int(comment="tenant_id"),
        "question_list": List(
            struct=[Dict(
                {"question_id": Str(comment="问题id"),
                 "question": Str(comment="问题"),
                 "answer": Str(comment="回答"),
                 "status": Int(comment="状态")},
                comment="问题")],
            comment="问题列表")
    })

    print(schema.validate(value))

    sub_schema = Dict(struct={"question_id": Str(comment="问题id"),
                              "question": Str(comment="问题"),
                              "answer": Str(comment="回答"),
                              "status": Int(comment="状态")},
                      comment="问题")
    schema = Dict({
        "user_id": Int(comment="用户id"),
        "tenant_id": Int(comment="tenant_id"),
        "question_list": List(
            struct=[sub_schema, ],
            comment="问题列表")
    })
    err, value = schema.validate(value)
