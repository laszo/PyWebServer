import re

pattern = '\w\s*\{.*\}';


def foo(fn):
    f = open(fn, 'rt')
    for i in f:
        line = i.strip()
        if not line.startswith('#'):
            if not line == '':
                yield line
    f.close()

def foo2(fn):
    for line in foo(fn):
        for i in line.split('}'):
            if i:
                yield ' '.join(i+'}'.split())

        # line = line.replace('{', ' {')
        # line = line.replace('}', ' }')
        # yield ' '.join(line.split())

def split(line, char):
    for i in line.split('}'):
        yield i + '}'

patd = r'(?P<directive>\w+(\s+\w+)+;)'
patc = r'(?P<context>\w+\s+\{.*\})';
compd = re.compile(patd)
compc = re.compile(patc)


bar = '\n'.join([i for i in foo('config.conf')])

# 彻底晕菜了！
for i in bar:
    print [split(i, '}')]

# print bar

import tools

main_context = tools.block()

# for i in foo('config.conf'):
#     main_context.push(i)

# for i in main_context.directives:
#     print i

