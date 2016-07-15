try:
    import _markerlib.markers
except ImportError:
    pass
else:
    class ReadOnlyDict(dict):

        def __init__(self, data):
            self.readonly = False
            super(ReadOnlyDict, self).__init__(data)

        def __setitem__(self, key, value):
            if not self.readonly:
                return super(ReadOnlyDict, self).__setitem__(key, value)


    # _markerlib.default_environment() obtains its data from _VARS
    env = _markerlib.markers._VARS
    for key in list(env.keys()):
        new_key = key.replace('.', '_')
        if new_key != key:
            env[new_key] = env[key]

    _markerlib.markers._VARS = ReadOnlyDict(env)

    def default_environment():
        print('getting default_environment', _markerlib.markers._VARS)
        return _markerlib.markers._VARS


    _markerlib.default_environment = default_environment

try:
    import pkg_resources
    del pkg_resources.parser
    pkg_resources.evaluate_marker = pkg_resources.MarkerEvaluation._markerlib_evaluate
    pkg_resources.MarkerEvaluation.evaluate_marker = pkg_resources.MarkerEvaluation._markerlib_evaluate
except (ImportError, AttributeError):
    pass

from setuptools import setup


def fread(fn):
    return open(fn, 'rb').read().decode('utf-8')

setup(
    name='tox-travis',
    description='Seamless integration of Tox into Travis CI',
    long_description=fread('README.rst') + '\n\n' + fread('HISTORY.rst'),
    author='Ryan Hiebert',
    author_email='ryan@ryanhiebert.com',
    url='https://github.com/ryanhiebert/tox-travis',
    license='MIT',
    version='0.4',
    package_dir={'': 'src'},
    py_modules=['tox_travis'],
    entry_points={
        'tox': ['travis = tox_travis'],
    },
    install_requires=['tox>=2.0'],
    extras_require={
        ':python_version=="3.2"': ['virtualenv<14'],
        ':platform_python_implementation=="PyPy" and python_version=="3.3"': ['virtualenv>=15.0.2'],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
