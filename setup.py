import sys

try:
    import _markerlib
except ImportError:
    pass
else:
    print('providing py3 compatible _markerlib_evaluate')
    def _markerlib_evaluate(cls, text):
        env = _markerlib.default_environment()
        print('markerlib env', env)
        for key in list(env.keys()):
            new_key = key.replace('.', '_')
            env[new_key] = env.pop(key)
        try:
            result = _markerlib.interpret(text, env)
        except NameError:
            e = sys.exc_info()[1]
            raise SyntaxError(e.args[0])
        return result

    try:
        import pkg_resources
        del pkg_resources.parser
        pkg_resources.MarkerEvaluation.evaluate_marker = classmethod(_markerlib_evaluate)
        pkg_resources.evaluate_marker = pkg_resources.MarkerEvaluation.evaluate_marker
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
