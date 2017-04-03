# coding:utf-8

__all__ = ['parse', 'EasyDict']

import os
import sys
import re
import six
import json5
from .easydict import EasyDict


def is_dict(v):
    return isinstance(v, dict)


def is_list(v):
    return isinstance(v, list)


def is_str(v):
    return isinstance(v, str)  # or isinstance(v, unicode)

_r_abs_path = re.compile(r'^(?:(?:file:/)?/|~)')


def is_abs_path(v):
    return _r_abs_path.match(v)

INCLUDE_KEY = u"__include__"
IMPORT_KEY = u"__import__"


def extend(target, source):
    for k in list(source.keys()):
        if is_dict(target[k]) and is_dict(source[k]):
            extend(target[k], source[k])
        else:
            target[k] = source[k]

##
# conf [list, dict]
# file_stack [list] 分析的文件栈
# base_path [str] 包含文件的相对路径
##


def merge_conf(conf, file_stack, base_path):

    def merge_item(val_conf):
        if is_dict(val_conf) or is_list(val_conf):
            return merge_conf(val_conf, file_stack, base_path)
        return val_conf

    def parse_require(include_file, results, way):
        if not include_file:
            raise Exception('%s error: %s' % (way, include_file))

        filename_parse = is_abs_path(include_file)
        if not filename_parse:
            include_file = os.path.join(base_path, include_file)
        elif filename_parse.group() == u'~':
            include_file = os.path.expanduser(include_file)

        include_file = os.path.normpath(include_file)
        # print(include_file)
        include_conf = eval_file_parse(include_file, file_stack)
        results.append(include_conf)

    if is_dict(conf):
        new_conf = EasyDict()
        imports = []
        includes = []

        import_files = conf.get(IMPORT_KEY)
        if import_files:
            conf.pop(IMPORT_KEY)
            if is_str(import_files):
                parse_require(import_files, imports, IMPORT_KEY)
            elif is_list(import_files):
                for f in import_files:
                    parse_require(f, imports, IMPORT_KEY)

        include_files = conf.get(INCLUDE_KEY)
        if include_files:
            conf.pop(INCLUDE_KEY)
            if is_str(include_files):
                parse_require(include_files, includes, INCLUDE_KEY)
            elif is_list(include_files):
                for f in include_files:
                    parse_require(f, includes, INCLUDE_KEY)

        for k, val in six.iteritems(conf):
            conf[k] = merge_item(val)

        if imports:
            for base_conf in imports:
                if is_dict(base_conf):
                    extend(new_conf, base_conf)

        extend(new_conf, conf)  # 当前配置覆盖默认配置

        if includes:
            for sub_conf in includes:
                if is_dict(sub_conf):
                    extend(new_conf, sub_conf)  # 合并

        return new_conf

    elif is_list(conf):
        for val in conf:
            merge_item(val)
        return conf
    else:
        pass


def eval_file_parse(abs_path_file, file_stack):
    if not os.path.isfile(abs_path_file):
        return None

    for f in file_stack:
        if f == abs_path_file:
            file_stack.append(abs_path_file)
            print_dependence_stack(file_stack)
            raise Exception('File cycle dependence!')

    file_stack.append(abs_path_file)

    # conf = None
    with open(abs_path_file, encoding='utf-8') as f:
        conf = json5.load(f, encoding='utf-8')
        if isinstance(conf, dict):
            conf = EasyDict(conf)
        conf = merge_conf(conf, file_stack, os.path.dirname(abs_path_file))

    file_stack.pop()

    return conf


def parse(filename):
    file_parse_stack = []

    filename_parse = is_abs_path(filename)
    if not filename_parse:
        filename = os.path.abspath(filename)
    elif filename_parse.group() == u'~':
        filename = os.path.expanduser(filename)

    return eval_file_parse(filename, file_parse_stack) or EasyDict()


def print_dependence_stack(arr):
    for i, abs_filename in enumerate(arr):
        label = u'==>' if i > 0 else u'   '
        print(u'%s %s' % (label, abs_filename))


# conf = parse(u'jsonnet_conf_text.json')
# import pprint; pprint.pprint(conf)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        import pprint
        pprint.pprint(parse(sys.argv[1]))
    else:
        print('usage: jsonconf somefile.json')
