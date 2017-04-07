# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe


setup(
    options = {'py2exe' : {
        'includes' : ['os', 'codecs', 're', 'copy', 'json'],
        'excludes' : ['readline'],
        'compressed' : 1,
        'optimize' : 2,
        'bundle_files' : 2,
        'dist_dir' : './',
    }},
    zipfile = None,
    console = ["main.py"],
    name = 'AutomaticLeagueGenerator'
    )
