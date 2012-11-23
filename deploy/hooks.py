import os
import logging
import glob

from yola.deploy.hooks.django import DjangoApp
from yola.deploy.hooks.htpasswd import AuthenticatedApp
from yola.deploy.hooks.upstart import UpstartApp
from yola.deploy.util import chown_r, touch

log = logging.getLogger(__name__)


class Hooks(AuthenticatedApp, DjangoApp, UpstartApp):
    migrate_on_deploy = True

    def prepare(self):
        super(Hooks, self).prepare()

        data_dir = os.path.join(self.root, 'data')
        webapp_dir = glob.glob(self.deploy_path('virtualenv', 'lib',
                                                'python2.*', 'site-packages',
                                                'graphite_web-*', 'webapp'))
        os.symlink(data_dir, self.deploy_path('storage'))
        os.symlink(webapp_dir[0], self.deploy_path('webapp'))
        os.symlink(self.deploy_path(self.app, 'conf'),
                   self.deploy_path('conf'))

        log_dir = self.config.graphite.path.log_dir
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        if not os.path.exists(os.path.join(log_dir, 'info.log')):
            touch(os.path.join(log_dir, 'info.log'))
        if not os.path.exists(os.path.join(log_dir, 'exception.log')):
            touch(os.path.join(log_dir, 'exception.log'))
        chown_r(log_dir, 'www-data', 'www-data')


hooks = Hooks
