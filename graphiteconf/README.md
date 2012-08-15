Since the graphite settings module does the following:

  from graphite.local_settings import *

And since we don't want to modify the package in-place in our virtualenv, I 
have had to create a separate "graphiteconf" package to import settings from.
I have duplicated the settings.py file from the graphite package to here and
made some modifications so that the paths work for us.  The original file is in
this directory with the name "settings.py.orig" for comparison - as we upgrade
through different versions of graphite, please keep these in sync.
