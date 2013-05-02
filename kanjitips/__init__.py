# -*- mode: python ; coding: utf-8 -*-
# © 2013 Roland Sieker <ospalh@gmail.com>
#
# This file: License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html
#

"""
Anki2 add-on to show ankit tooltips (bubble help).
"""

from .tips import setup_tips

__version__ = '0.0a1'
#__all__ = ['setup_tips', 'show_tips', '__version__']

setup_tips()
