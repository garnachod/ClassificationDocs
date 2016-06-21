#!/usr/bin/env python

from distutils.core import setup

setup(name='ClassificationDocs',
      version='1.0',
      description='API for Classification Docs',
      author='Daniel Garnacho',
      author_email='garnachod@gmail.com',
      packages=['Config', 'DBWrapper', 'Train', 'TextProcessing', 'LuigiTasks'],
      package_dir={},
    )