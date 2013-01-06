from string import Template
import subprocess
import inspect

class NamespaceMeta(type):
    def __getitem__(self, arg):
        return getattr(self, arg)

class Namespace(object):
    __metaclass__ = NamespaceMeta


'''
run a command line using bash -c
ns: the namspace or dictionary object
'''
def cmd_run(cmd, ns=None):
    d = {}
    fr = inspect.currentframe().f_back
    d.update(fr.f_locals)
    d.update(fr.f_globals)

    if ns is None:
        pass
    elif issubclass(ns, Namespace):
        d.update(map(lambda k: (k, getattr(ns, k)), dir(ns)))
    # treat ns as dictionary
    else:
        d.update(ns)

    cmd = Template(cmd.strip()).substitute(d)
    # print cmd
    return subprocess.call(['bash', '-exc', cmd])        

def sub(s, ns=None):
    d = {}
    fr = inspect.currentframe().f_back
    d.update(fr.f_globals)
    d.update(fr.f_locals)

    if ns is None:
        pass
    elif issubclass(ns, Namespace):
        d.update(map(lambda k: (k, getattr(ns, k)), dir(ns)))
    # treat ns as dictionary
    else:
        d.update(ns)

    s = Template(s).substitute(d)    
    return s

'''
count lines of a given file: wc -l
'''
def count_lines(fname):
    k = 0
    with open(fname) as fi:
        for line in fi:
            k += 1
    return k

def _test():
    class Variables:
        msg = "world"

    cmd_run('echo $msg $msg2', Variables)

if __name__ == '__main__':
    msg2 = "hello"
    _test()

    class Full(Namespace):
        b = 1
    
    print Full.b, Full["b"]
