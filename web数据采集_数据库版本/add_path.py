from subprocess import Popen, PIPE
import os
import sys
"""
def add_path():
    print sys.stdout.encoding
    proc = Popen(['wmic', 'process'], stdout = PIPE, stderr = PIPE)
    #print "wait"
    return_code = proc.wait()
    voutput = proc.stdout.read()
    print voutput
    if return_code == 0:
        return True
    #elif return_code == -999:
    #    print 'not set:', voutput
    else:
        print "Failure %s:\n%s" % (return_code, voutput)
        return False
"""
def add_path():
    cwd = os.getcwd()
    env = os.environ['PATH']
    os.environ['PATH'] = cwd + ";"+ env
    
    #env = os.environ['PATH']
    #print env
   

def test():
    add_path()
    #print env

if __name__ == '__main__':
    test()