# sheldon woodward
# 2/25/18

"""Setuptools File"""

from os.path import abspath, dirname, join
from setuptools import setup


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup_requires = [
    'setuptools_scm'
]

install_requires = [
    'bitmath',
    'iso-639',
    'bcp47'
]


setup(
    name='pymkv',
    description='A Python wrapper for mkvmerge. It provides support for muxing, splitting, linking, chapters, tags, '
                'and attachments through the use of mkvmerge.',
    long_description=long_description,
    url='https://github.com/sheldonkwoodward/pymkv',
    author='Sheldon Woodward',
    author_email='me@sheldonw.com',
    license='MIT',
    packages=['pymkv'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Video :: Conversion',
        'Topic :: Utilities',
    ],
    keywords='wrapper',
    python_requires='>=3.9',
    use_scm_version=True,
    setup_requires=setup_requires,
    install_requires=install_requires,
)
