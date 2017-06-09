from subprocess import Popen, PIPE

#proc = Popen(['tracert','www.baidu.com'], stdout=PIPE, stderr=PIPE)
#proc = Popen(['ping','www.baidu.com'], stdout=PIPE, stderr=PIPE)
#ipconfig /flushdns
def clear_dns():
    #return_code = -999 
    proc = Popen(['ipconfig', '/flushdns'], stdout = PIPE, stderr = PIPE)
    #print "wait"
    return_code = proc.wait()
    voutput = proc.stdout.read()
    if return_code == 0:
        return True
    #elif return_code == -999:
    #    print 'not set:', voutput
    else:
        #print "Failure %s:\n%s" % (return_code, voutput)
        return False