import os
import imp

from settingslib.compat import execfile


def get_module_from_file_path(path):
    mod = imp.new_module('settings')
    mod.__file__ = path
    execfile(path, mod.__dict__)
    return mod


def get_module_from_dotted_path(path):
    bits = path.split('.')
    
    file_path = imp.find_module(bits[0])[1]
    
    for bit in bits[1:]:
        file_path = imp.find_module(bit, [file_path])[1]

    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, '__init__.py')
    
    return get_module_from_file_path(file_path)


def import_attribute(name):
    '''Import attribute by string reference. Throw ImportError
    or AttributeError if module or attribute does not exist.
    
    '''
    i = name.rfind(':')
    
    module, attr = name[:i], name[i+1:]
    mod = __import__(module, globals(), locals(), [attr])

    return getattr(mod, attr)


def get_dict_iterator(dict):
    if hasattr(dict, 'iteritems'):
        return dict.iteritems()
    return dict.items()


def get_object_iterator(obj):
    for key in dir(obj):
        if is_valid_key(key):
            yield key, getattr(obj, key)


def is_valid_key(key):
    if key.startswith('_'):
        return False

    if key.isupper():
        return True

    return False

