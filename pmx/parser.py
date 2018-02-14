"""Some functions to write parsers for different data formats.

Usage:

>>> lst = open(infile,'r').readlines()     # read file
>>> lst = kickOutComments(lst,'#')       # remove comments with # or ;
>>> lst = parseList('ifs',lst)            # parse each line and return
[integer, float, string] triples


>>> subl = readSection(lst,'[ begin ]','[ end ]') # get all lines between
[ begin ] and [ end ]
"""

from collections import OrderedDict


class ParserError(Exception):

    def __init__(self, s):
        self.s = s

    def __str__(self):
        return repr(self.s)


def kickOutComments(lines, comment='#'):
    ret = []
    for line in lines:
        if comment in line:
            idx = line.index(comment)
            new_line = line[:idx].strip()
            if new_line:
                ret.append(new_line)
        else:
            new_line = line.strip()
            if new_line:
                ret.append(new_line)
    return ret


def readSection(lines, begin, end):
    ret = []
    for i, line in enumerate(lines):
        if line.strip() == begin:
            for line2 in lines[i+1:]:
                if end not in line2:
                    ret.append(line2)
                else:
                    return ret
    return ret


def __parse_error(msg, line):
    s = "pmx_Error_> %s" % msg
    s += "\nTrouble is here -> %s" % line
    raise ParserError(s)


def __parse_entry(entr, tp):
    new = None
    if tp == 's':
        new = entr
    elif tp == 'i':
        try:
            new = int(entr)
        except:
            __parse_error("Integer conversion failed", entr)
    elif tp == 'f':
        try:
            new = float(entr)
        except:
            __parse_error("Float conversion failed", entr)
    return new


def parseList(format_string, lst, ignore_missing=False):
    ret = []
    format_list = [a for a in format_string]
    for line in lst:
        entr = line.split()
        if len(entr) != len(format_list):
            if not ignore_missing or len(entr) < len(format_list):
                __parse_error("Cannot convert line into format: %s" %
                              format_string, line)
        new_list = []
        for i, tp in enumerate(format_list):
            new_list.append(__parse_entry(entr[i], tp))
        ret.append(new_list)
    return ret


def read_and_format(filename, format_string, comment='#',
                    ignore_missing=False):
    l = open(filename).readlines()
    if comment is not None:
        l = kickOutComments(l, comment)
    n = parseList(format_string, l, ignore_missing)
    return n


# ------------------------------------------
# some file format parsers frequently needed
# ------------------------------------------
def read_fasta(fn):
    l = open(fn).readlines()
    l = kickOutComments(l)
    dic = OrderedDict()
    name = None
    for line in l:
        if line.startswith('>'):
            if name is not None:
                dic[name] = new_s
            new_s = ''
            name = line[1:].strip()
        else:
            seq = line.strip().upper()
            new_s += seq
    dic[name] = new_s
    return dic


def read_xvg(fn,  style='xy'):
    l = open(fn).readlines()
    l = kickOutComments(l, '@')
    l = kickOutComments(l, '#')
    l = kickOutComments(l, '&')
    res = parseList('ff', l)
    if style == 'list':
        return res
    else:
        x = map(lambda a: a[0],  res)
        y = map(lambda a: a[1],  res)
        return x,  y
