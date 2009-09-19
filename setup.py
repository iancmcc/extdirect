from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='zenoss.extdirect',
      version=version,
      description="Python implementation of an Ext.Direct router",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ian McCracken',
      author_email='ian@zenoss.com',
      url='',
      license='GPLv2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['zenoss'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
