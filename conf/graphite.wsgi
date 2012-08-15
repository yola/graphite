import glob
import os
import site
import sys

app = 'graphite'
install_root = os.path.join("{{conf.deploy.root}}", app, 'live')

sys.path.append(os.path.join(install_root, app))
for dir_ in glob.glob(os.path.join(install_root, 'virtualenv', 'lib',
                                   'python2.*', 'site-packages')):
    site.addsitedir(dir_)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# Preload the index (called by WSGIImportScript in the apache vhost)
from graphite.logger import log
log.info("graphite.wsgi - pid %d - reloading search index" % os.getpid())
import graphite.metrics.search
