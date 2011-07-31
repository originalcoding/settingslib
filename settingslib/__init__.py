'''Settings wrapper.'''


__version__ = '0.7.1'
__author__ = 'Pavlo Kapyshin'
__email__ = 'i@93z.org'


import os
import copy
import types

from settingslib.compat import UserDict, basestring
from settingslib.utils import (
    import_attribute,
    
    get_module_from_file_path,
    get_module_from_dotted_path,
    
    get_dict_iterator,
    get_object_iterator,

    is_valid_key
)


class Settings(dict):
    '''Provides way to retrieve settings from objects and .py files.'''

    def __init__(self, *args, **kw):
        for arg in args:
            self._handle_arg(arg)
        self._handle_arg(kw)

    def __setitem__(self, key, value):
        if is_valid_key(key):
            self._setitem(key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        object.__delattr__(self, key)

    def __setattr__(self, name, value):
        if is_valid_key(name):
            self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)

    def __add__(self, other):
        settings = self.copy()
        settings.update(other)
        return settings

    def _setitem(self, key, value):
        object.__setattr__(self, key, value)
        dict.__setitem__(self, key, value)

    def _handle_arg(self, arg):
        sequence = None

        if not arg:
            return

        if isinstance(arg, UserDict):
            sequence = get_dict_iterator(arg.data)
        
        elif isinstance(arg, dict):
            sequence = get_dict_iterator(arg)
        
        elif isinstance(arg, types.ModuleType):
            sequence = get_dict_iterator(arg.__dict__)
        
        elif isinstance(arg, basestring):
            if arg.isupper() and arg in os.environ:
                obj = os.environ[arg]
            
            elif os.sep in arg:
                path = os.path.expanduser(arg)
                obj = get_module_from_file_path(path)

            elif ':' in arg:
                path, obj_name = arg.split(':', 1)
                mod = get_module_from_dotted_path(path)
                obj = getattr(mod, obj_name)
            
            else:             
                obj = get_module_from_dotted_path(arg)
            
            return self._handle_arg(obj)
        
        elif hasattr(arg, '__iter__'):
            sequence = arg.__iter__()
        
        else:
            sequence = get_object_iterator(arg)

        for key, value in sequence:
            if is_valid_key(key):
                self._setitem(key, value)

    def get(self, key, default=None, imp=False):
        if key in self:
            value = self[key]
        else:
            value = default

        if imp and isinstance(value, basestring):
            value = import_attribute(value)
        
        return value
    
    def update(self, dict=None, **kw):
        if dict:
            self._handle_arg(dict)

        if kw:
            self.update(kw)

    def copy(self):
        return copy.copy(self)

