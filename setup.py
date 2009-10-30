from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='ftw.dashboard.portlets.favourites',
      version=version,
      description="A Favourite Portlet, wich show your favourites on your dashboard",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='philippegross',
      author_email='mailto:info@4teamwork.ch',
      url='http://plone.org/products/ftw.dashboard.portlets.favourites/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
		  'collective.js.jqueryui==1.7.2.5',
          # -*- Extra requirements: -*- 
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
