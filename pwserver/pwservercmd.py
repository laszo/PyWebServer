import sys
# import server
# from server import launch

def start():
    pass

def reload():
    pass

def wsgi():
    pass

def main():
    print sys.argv
    print globals()
    print locals()
    import signal
    signal.signal(signal.SIGUSR1, suser1)
    import time
    import os
    num = 0
    while True:
        print 'run time: %d' % num
        num += 1
        time.sleep(3)
        if SHOULD_BREAK:
            break
        print 'run again, pid: %d' % os.getpid()

SHOULD_BREAK = False

def suser1(signum, frame):
    print 'geting signal SIGUSR1'
    global SHOULD_BREAK
    SHOULD_BREAK = True

if __name__ == '__main__':
    main()
