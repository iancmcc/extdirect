from setuptools import setup, find_packages
import sys, os

version = '0.3'

setup(name='extdirect',
      version=version,
      description="Python implementation of an Ext.Direct router",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ian McCracken',
      author_email='ian@zenoss.com',
      url='http://code.google.com/p/extdirect',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
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
