import os, sys

SPLIT_STR = '/'
if os.name == 'nt':
    SPLIT_STR = '\\'

RPATH = os.path.realpath(__file__)
PPATH =  SPLIT_STR.join(RPATH.split(SPLIT_STR)[:-1])
PWS_PATH = os.path.join(PPATH, os.path.pardir)

sys.path.append(PWS_PATH)

import pwserver

if __name__ == '__main__':
    pwserver.server.launch(cfg_file=os.path.join(PPATH, 'config.conf'))
