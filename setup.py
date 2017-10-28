"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from discover import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(
    name = 'discover black',
    version = __version__,
    description = 'A NLP receiver + Knowledge Graph searcher. For Discover. @HackTX',
    long_description = long_description,
    url = 'https://github.com/askalburgi/discover_black',
    author = 'Arjun Kalburgi',
    author_email = 'askalburgi@gmail.com',
    license = 'UNLICENSE',
    classifiers = [
        'Intended Audience :: N/A',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs']),
    install_requires = ['docopt'],
    extras_require = {
        # 'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'discover=discover.cli:main',
        ],
    },
    # cmdclass = {'test': RunTests},
)
