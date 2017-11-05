import os
from setuptools import setup
from codesearch import __version__


def read(filename):
  """
  Utility function to read the README file, used for the long_description.
  It's nice, because now
  1) we have a top level README file and
  2) it's easier to type in the README file than to put a raw string in below.

  :param filename: The name of the file to read from.
  :return: The contents of the file.
  """
  return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='codesearch',
    version=__version__,
    description='A command-line tool for searching for code patterns within your git repository.',
    packages=['codesearch'],
    install_requires=[
        'PyYAML>=3.12',
    ],
    long_description=read('README.md'),
    classifiers=[],
    entry_points={
        'console_scripts': [
            'codesearch = codesearch:run'
        ]
    },

    # PyPI metadata
    author='Aleksandar Gyorev',
    author_email='alexander.gyorev@gmail.com',
    license='MIT License',
    keywords='code search snippets git repository project',
    url='http://github.com/agyorev/codesearch',
)
