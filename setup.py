import os, sys
if sys.version_info >= (3,0):
    from distribute_setup import use_setuptools
    use_setuptools()
from setuptools import setup

long_description = """
pylib: cross-python development utils

Platforms: Linux, Win32, OSX

Interpreters: Python versions 2.4 through to 3.2, Jython 2.5.1 and PyPy

Web page: http://pylib.org

Bugs and issues: http://bitbucket.org/hpk42/pylib/issues/

Mailing lists and more contact points: http://pylib.org/contact.html

(c) Holger Krekel and others, 2004-2010
"""
def main():
    setup(
        name='pylib',
        description='pylib: cross-python path, io, code, log facilities',
        long_description = long_description,
        install_requires=['py>=1.3.9', ], # force newer py version which removes 'py' namespace
        #                                  # so we can occupy it
        version= '2.0.0.dev0',
        url='http://pylib.org',
        license='MIT license',
        platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
        author='holger krekel, Guido Wesdorp, Carl Friedrich Bolz, Armin Rigo, Maciej Fijalkowski & others',
        author_email='holger at merlinux.eu',
        classifiers=['Development Status :: 6 - Mature',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Software Development :: Testing',
                     'Topic :: Software Development :: Libraries',
                     'Topic :: Utilities',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3'],
        packages=['py',
                  'py._code',
                  'py._compat',
                  'py._io',
                  'py._log',
                  'py._path',
                  'py._process',
        ],
        zip_safe=False,
    )

if __name__ == '__main__':
    main()

