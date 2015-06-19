#!/usr/bin/env python

'''The setup and build script for the lightning-python library.'''

__author__ = 'github@mathisonian.com'
__version__ = '1.0.7'

# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
  name = "lightning-python",
  version = __version__,
  packages = ['lightning','lightning.types','lightning.lib'],
  author='Matthew Conlen',
  author_email='github@mathisonian.com',
  description='A Python client library for the Lightning data vizualization server',
  license='MIT',
  url='https://github.com/lightning-viz/lightning-python',
  keywords='lightning data data-viz',
)

# Extra package metadata to be used only if setuptools is installed
SETUPTOOLS_METADATA = dict(
  install_requires = open('requirements.txt').read().split(),
  include_package_data = True,
  package_data = {'lightning.lib': ['template.html']}
)

def Read(file):
  return open(file).read()

def BuildLongDescription():
  return '\n'.join([Read('README.md')])

def Main():
  # Use setuptools if available, otherwise fallback and use distutils
  try:
    import setuptools
    METADATA.update(SETUPTOOLS_METADATA)
    setuptools.setup(**METADATA)
  except ImportError:
    print("Could not import setuptools, using distutils")
    print("NOTE: You will need to install dependencies manualy")
    import distutils.core
    distutils.core.setup(**METADATA)

if __name__ == '__main__':
  Main()