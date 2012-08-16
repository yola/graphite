import os
import logging
import glob
import subprocess

from yola.deploy.hooks.configurator import ConfiguratedApp
from yola.deploy.hooks.python import PythonApp
from yola.deploy.hooks.templating import TemplatedApp
from yola.deploy.util import chown_r

log = logging.getLogger(__name__)


class Hooks(ConfiguratedApp, PythonApp, TemplatedApp):

    def __init__(self, *args, **kwargs):
        super(Hooks, self).__init__(*args, **kwargs)

    def prepare(self):
        super(Hooks, self).prepare()
        if self.config is None:
            raise Exception("Config hasn't been loaded yet")

        data_dir = os.path.join(self.root, 'data')
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        chown_r(data_dir, 'www-data', 'www-data')

        webapp_dir = glob.glob(self.deploy_path('virtualenv', 'lib',
                                                'python2.*', 'site-packages',
                                                'graphite_web-*', 'webapp'))

        os.symlink(data_dir, self.deploy_path('storage'))
        os.symlink(webapp_dir[0], self.deploy_path('webapp'))

        self.template('apache2/vhost.conf.template',
                      os.path.join('/etc/apache2/sites-enabled', self.app))
        self.template('graphite.wsgi.template', self.deploy_path('graphite', 
                                                    'conf', 'graphite.wsgi'))
        self.template('upstart-carbon.conf.template', '/etc/init/carbon.conf')

    def deployed(self):
        super(Hooks, self).deployed()
        try:
            subprocess.call(('service', 'carbon', 'stop'))
            subprocess.check_call(('service', 'carbon', 'start'))
        except subprocess.CalledProcessError:
            log.error("Unable to restart carbon")

hooks = Hooks
