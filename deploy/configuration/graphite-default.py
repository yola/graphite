import os

from yoconfigurator.dicts import merge_dicts, MissingValue


def update(config):
    data_path = os.path.join(config.deploy.root, 'graphite', 'data')
    new = {
        'graphite': {
            'path': {
                'data': data_path,
                'log_dir': '/var/log/graphite',
            },
            'db': {
                'name': os.path.join(data_path, 'graphite.sqlite'),
                'engine': 'django.db.backends.sqlite3',
                'user': '',
                'password': '',
                'host': '',
                'port': '',
            },
            'domain': 'graphite.%s' % config.common.domain.services,
            'htpasswd': {
                'users': {
                    'yola': MissingValue(),
                },
            },
            'ssl': config.common.wild_ssl_certs.services,
        },
    }
    return merge_dicts(config, new)
