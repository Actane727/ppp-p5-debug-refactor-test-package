"""Setup script for the shoppinglistapp package."""
from setuptools import setup


setup(name='shoppinglistapp',
      version='1.0.0',
      description='Shopping List App',
      url='https://whatever.org/',
      author='Brian Anderson',
      author_email='bri2369395@maricopa.edu',
      packages=['shoppinglistapp', 'shoppinglistapp.core'],
      include_package_data=True,
      zip_safe=False)
