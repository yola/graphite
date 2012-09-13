import os

from yola.configurator.dicts import merge_dicts


def update(config):
    data_path = os.path.join(config.deploy.root, 'graphite', 'data')
    new = {
        'graphite': {
            'path': {
                'data': data_path,
                'log': '/var/log/graphite.log',
            },
            'domain': 'graphite.%s' % config.common.domain.services,
            'htpasswd': {
                'users': {
                    'user': 'MissingValue(graphite.htpasswd.users.user)',
                    'password': 'MissingValue(graphite.htpasswd.users.password)',
                 },
            },
        },
    }
    return merge_dicts(config, new)
