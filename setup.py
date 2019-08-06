# sheldon woodward
# 2/25/18

"""Setuptools File"""

from os.path import abspath, dirname, join
from setuptools import setup


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

install_requires = [r.rstrip('\n') for r in open('requirements.txt').readlines()]


setup(
    name='pymkv',
    description='A Python wrapper for mkvmerge. It provides support for muxing tracks together, combining multiple '
                'MKV files, reordering tracks, naming tracks, and other MKV related things.',
    long_description=long_description,
    url='https://github.com/sheldonkwoodward/pymkv',
    author='Sheldon Woodward',
    author_email='admin@sheldonw.com',
    license='MIT',
    packages=['pymkv'],
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='wrapper',
    python_requires='>=3.6',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=install_requires,
)
