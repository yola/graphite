import os
import logging

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

    def deployed(self):
        super(Hooks, self).deployed()

hooks = Hooks
