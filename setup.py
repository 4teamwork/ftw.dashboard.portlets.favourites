import os
from setuptools import setup, find_packages


version = '3.5.1.dev0'
mainainter = 'Philipp Gross'
tests_require = [
    'plone.app.testing',
    'ftw.testing',
    'ftw.builder',
    'ftw.testbrowser',
    'plone.app.contenttypes',
    'mocker',
    ]

setup(name='ftw.dashboard.portlets.favourites',
      version=version,
      description="A favourite Portlet",
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 5.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw dashboard portlet favourites favorites',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.dashboard.portlets.favourites',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', 'ftw.dashboard', 'ftw.dashboard.portlets'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'ftw.dashboard.dragndrop>=2',
        'ftw.upgrade',
        'plone.api'
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
