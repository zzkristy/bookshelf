# coding: utf-8

import re
import os

__all__ = ['Conf']


def is_terminator(c):
    if c == ':' or c == '=' or c == ' ':
        return True
    return False


class ConfParse(object):

    def __init__(self, filename, resolve_ref=True):
        self.options = {}
        self.messages = []
        self.parse(filename)
        if resolve_ref:
            self.resolve_reference()

    def get(self, key, default_value="", resolve_ref=False):
        key = key.lower()
        value = self.options.get(key, default_value)
        if resolve_ref:
            ref = re.match(".*\\{\\{(.*?)\\}\\}", value)
            if not ref:
                return value
            ref_val = ref.group(1).strip()
            pos1 = value.find('{')
            pos2 = value.rfind('}') + 1
            prefix = value[:pos1]
            lastfix = value[pos2:]
            if ref_val != key:
                rv = self.get(ref_val, default_value, resolve_ref)
                self.options[key] = prefix + rv + lastfix
                return rv
        else:
            return value

    def get_values(self, key):
        val = self.get(key)
        vals = [v.strip() for v in val.split(',')]
        return vals

    def get_all(self):
        return self.options

    def ignore_comment_and_ter(self, line):
        new_line = ''
        flag = 1
        for index, c in enumerate(line):
            if (c == '#' and index == 0) or c == ';':
                break
            if flag != 4:
                if is_terminator(c):
                    c = ' '
                    flag = 2
                elif flag == 2:
                    flag = 4
                if new_line and new_line[-1] == ' ' and c == ' ':
                    continue
            new_line += c
        return new_line.strip()

    def parse(self, filename):
        try:
            f = open(filename, 'r', encoding='utf-8')
        except Exception:
            return
        for line in f:
            line = self.ignore_comment_and_ter(line)
            if not line:
                continue
            i = line.find(' ')
            if i == -1:
                key = line
                val = ''
            else:
                key = line[:i]
                val = line[i + 1:]
            if not val:
                val = ''
            if key == 'include':
                path = val
                if not os.path.isabs(path):
                    path = os.path.dirname(os.path.abspath(filename)) + '/' + val
                self.parse(path)
            else:
                self.options[key] = val

    def resolve_reference(self):
        for key in self.options:
            self.get(key, "", True)


class Conf(object):

    def __init__(self, filename):
        self._conf = ConfParse(filename)
        self.local_conf = {}

    def get_values(self, key):
        val = self.local_conf.get(key)
        if val:
            return [p.strip() for p in val.split(',')]
        return list(self._conf.get_values(key))

    def get(self, key, val=''):
        local_val = self.local_conf.get(key)
        if local_val:
            return local_val
        return self._conf.get(key, val)

    def get_all(self):
        all_conf = self._conf.get_all()
        real_all_conf = {}
        for key, value in all_conf.items():
            real_all_conf[key] = value
        real_all_conf.update(self.local_conf)
        return real_all_conf

    def __getattr__(self, name):
        try:
            return super(Conf, self).__getattr__(name)
        except Exception:
            return self.get(name)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if os.access(filename, os.F_OK):
            conf = Conf(filename)
            options = conf.get_all()
            import pprint
            pprint.pprint(options)
            # for key in options:
            # print("%s=%s" % (key, options[key]))
