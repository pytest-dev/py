import os, sys

try:
    from setuptools import setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

def main():
    setup(
        name='py',
        description='library with cross-python path, ini-parsing, io, code, log facilities',
        long_description = open('README.txt').read(),
        version='1.4.7',
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
                  'py._io',
                  'py._log',
                  'py._path',
                  'py._process',
        ],
        zip_safe=False,
    )

if __name__ == '__main__':
    main()