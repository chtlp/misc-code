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
    elif '__getitem__' in dir(ns):
        d.update(ns)
    else:
        d.update(map(lambda k: (k, getattr(ns, k)), dir(ns)))

    cmd = Template(cmd.strip()).substitute(d)
    # print cmd
    return subprocess.call(['bash', '-exc', cmd])        


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
