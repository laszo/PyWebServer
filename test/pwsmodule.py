import sys

def pwpath():
    import os
    SPLIT_STR = '/'
    if os.name == 'nt':
        SPLIT_STR = '\\'

    RPATH = os.path.realpath(__file__)
    PPATH =  SPLIT_STR.join(RPATH.split(SPLIT_STR)[:-1])
    PWS_PATH = os.path.join(PPATH, os.path.pardir)
    RPWPATH = os.path.realpath(PWS_PATH)
    return RPWPATH

sys.path.append(pwpath())

import pwserver

if __name__ == '__main__':
    print globals()
    # pwserver.server.launch(cfg_file=os.path.join(PPATH, 'config.conf'))
