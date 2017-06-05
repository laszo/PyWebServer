#! --encoding:utf8--

import re

pattern = '\w\s*\{.*\}';


def foo(fn):
    f = open(fn, 'rt')
    for i in f:
        line = i.strip()
        if not line.startswith('#'):
            if not line == '':
                line = line.replace('{', '{\n')
                line = line.replace(';', ';\n')
                line = line.replace('}', '\n}\n')
                for j in line.split('\n'):
                    if len(j) > 0:
                        yield j
    f.close()

# outfile = open('out.conf', 'wt')
# for i in foo('config.conf'):
#     outfile.write(i)
# outfile.flush()
# outfile.close()

import tools


def main():
    main_context = tools.block()
    for i in foo('out.conf'):
        main_context.push(i)
    print main_context
    for i in main_context.find('http.include'):
        print i
    print '-------------------------------------'
    for i in main_context.find('http.server.listen'):
        print i
    print '-------------------------------------'
    for i in main_context.find('http.server'):
        for j in i.find('location'):
            print j
        for j in i.find('listen'):
            print j

if __name__ == '__main__':
    main()
