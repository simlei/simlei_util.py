from setuptools import setup

requirements = [
    'attrs',
    'funcy'
]

setup(name='simlei_util',
      version='0.0.1',
      description='utilities for local python development',
      author='Simon Leischnig',
      author_email='simonjena@gmail.com',
      package_dir={'': 'src'},
      packages=['sutil'],
      install_requires=requirements
      )
