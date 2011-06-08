try:
    from UserDict import UserDict
except ImportError:
    from collections import UserDict

try:
    basestring = basestring
except NameError:
    basestring = str

try:
    execfile = execfile
except NameError:
    def execfile(fn, globals):
        f = open(fn)
        source = f.read()
        f.close()
        code = compile(source, fn, 'exec')
        exec(code, globals)

