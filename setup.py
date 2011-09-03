#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see http://docs.python.org/distutils/

from distutils.core import setup
import piebookData
setup(name = piebookData.NAME,
      version = piebookData.VERSION,
      description = piebookData.DESCRIPTION,
      author = 'Louis Taylor',
      author_email = 'kragniz@gmail.com',
      license = 'GPL v3 or later',
      packages = ['piebookData'],
      scripts = ['piebook'],
      requires = ['curses']
      )
