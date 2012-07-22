|lib|
~~~~~

Easy to use settings wrapper that supports settings loading from objects,
.py files, etc. Works with Python 2.5 and higher.


How to use it?
==============

|cls| class is what you import when you want to use this library::

    from settingslib import Settings


Arguments
---------

Then you pass arguments that contain things class knows how to load data from::

    >>> Settings({})  # if you can, use Settings() instead of empty arguments
    {}

    >>> Settings({'FOO': 'bar'})
    {'FOO': 'bar'}

|cls| ignores keys that start with ``_`` (underscore) or are not uppercase
(i.e. ``key.isupper()`` is ``False``)::

    >>> Settings({'FOO': 'bar', 'a': 1})
    {'FOO': 'bar'}

    >>> Settings({'FOO': 'bar', 'A': 1})
    {'A': 1, 'FOO': 'bar'}

    >>> Settings(
    ...     ImportError,
    ...     [],
    ...     lambda: 'test',
    ...     type,
    ...     int,
    ...     all,
    ...     '',
    ...     (),
    ...     Settings()
    ... ) == Settings()
    True

You can pass multiple arguments as well::

    >>> Settings({'FOO': 'bar'}, {'A': 1})
    {'A': 1, 'FOO': 'bar'}


|cls| can accept one or many arguments of the following types:


- keyword argument::

    >>> Settings(A=1, FOO='bar')
    {'A': 1, 'FOO': 'bar'}

- dict::

    >>> Settings({'A': 1, 'FOO': 'bar'})
    {'A': 1, 'FOO': 'bar'}

- generator::

    >>> def test():
    ...     yield ('A', 1)
    ...     yield ('FOO', 'bar')
    ... 
    >>> Settings(test())
    {'A': 1, 'FOO': 'bar'}

- list or tuple::

    >>> Settings([('A', 1), ('FOO', 'bar')])
    {'A': 1, 'FOO': 'bar'}

    >>> Settings((('A', 1), ('FOO', 'bar')))
    {'A': 1, 'FOO': 'bar'}

- class::

    >>> class Test(object):
    ...     A = 1
    ...     FOO = 'bar'
    ... 
    >>> Settings(Test)
    {'A': 1, 'FOO': 'bar'}

- instance of class::

    >>> class Test(object):
    ...     A = 1
    ...     FOO = 'bar'
    ... 
    >>> Settings(Test())
    {'A': 1, 'FOO': 'bar'}

- module::

    >>> import django
    >>> Settings(django)
    {'VERSION': (1, 3, 1, 'final', 0)}

- module_name (known as "dotted path")::

    >>> Settings('django')
    {'VERSION': (1, 3, 1, 'final', 0)}

    >>> Settings('django.utils.http')
    {'ASCTIME_DATE': re.compile(r'...'),
     'ETAG_MATCH': re.compile(r'...'),
     'MONTHS': ['jan',
      'feb',
      'mar',
      'apr',
      'may',
      'jun',
      'jul',
      'aug',
      'sep',
      'oct',
      'nov',
      'dec'],
     'RFC1123_DATE': re.compile(r'...'),
     'RFC850_DATE': re.compile(r'...')}

- module_name.may.be.nested:object_name::

    >>> Settings('some.path:some_arg')
    {'A': 1, 'FOO': 'bar'}

- environment variable's name (can "contain" only string type, obviously)::

    >>> import os
    >>> os.environ['SOME_ENV_VAR'] = 'django'
    >>> Settings('SOME_ENV_VAR')
    {'VERSION': (1, 3, 1, 'final', 0)}

- path to .py file (must contain ``os.sep``; e.g. "./somecfg.py")::

    >>> Settings('/usr/local/lib/python2.7/dist-packages/django/__init__.py')
    {'VERSION': (1, 3, 1, 'final', 0)}


Data manipulation
-----------------

Aforementioned settings class is subclass of ``dict`` Python built-in type, thus
result of the following expression is ``True``::


    (Settings({}) == {}) == (not bool(Settings({})))

It supports usual ``dict``-style operations.

::

    >>> limits = Settings(CPU1=40, CPU2=42, CPU3=74, CPU4=70)


Get::

    >>> limits['CPU1']
    40

    >>> limits.get('CPU1')
    40

    >>> limits['123']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: '123'

There is, though, one extension to ``get`` method: ``imp`` argument. Let's
create settings::

    >>> s = Settings(TEMPLATE_LOADER='mytemplateengine.loaders:MegaLoader')

Usual ``get`` will give you what you expect::

    >>> s.get('TEMPLATE_LOADER')
    'mytemplateengine.loaders:MegaLoader'

What about getting actual object from known dotted path? Mighty class |cls|
can do that for you::

    >>> s.get('TEMPLATE_LOADER', imp=True)
    <class 'mytemplateengine.loaders.MegaLoader'>

Django uses similar settings storage method for ``EMAIL_BACKEND``,
``MESSAGE_STORAGE``, ``MIDDLEWARE_CLASSES``, etc.


Set::

    >>> limits['CPU5'] = 100


Update::

    >>> limits.update(CPU5=50)

Note that ``update`` method supports same variety of argument types as
``__init__`` of |cls| class does, but only one positional argument.


Delete::

    >>> del limits['CPU5']
    >>> limits['CPU5']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'CPU5'


Copy::

    >>> limits.copy() is limits
    False

    >>> limits.copy() == limits
    True


Also you can add settings::

    >>> limits + Settings({'HELLO': 'SETTINGS!'})
    {'CPU4': 70, 'CPU2': 42, 'CPU3': 74, 'HELLO': 'SETTINGS!', 'CPU1': 40}

Note that this did not modify original ``limits``.


How to get help?
================

Email: i@93z.org.

GitHub: http://github.com/kapishin/settingslib/.

Also see `my notes about it <http://93z.org/settingslib/>`_.


.. |lib| replace:: ``settingslib``
.. |cls| replace:: ``settingslib.Settings``

