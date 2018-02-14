'''
pip install
'''

import glob
from setuptools import setup


setup(name='CobraUtils', version='0.1.0', license='MIT',
      url='https://github.com/cimbs/cobra_services',
      author='Dimitri Coukos',
      author_email='dimitri.coukos@epfl.ch',
      description='Information for cobra models.',
      packages=['cobra_services'],
      scripts=glob.glob("bin/*.py") + glob.glob("bin/*.sh"),
      long_description=open('README.md').read(),
      zip_safe=False,
      setup_requires=['cobra'],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True)
