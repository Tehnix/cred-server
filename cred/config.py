"""
The configuration files are searched for in the following order:
    1. Local directory
    2. Users home directory
    3. Users app directory
    4. System app directory

The file searched for is called .credrc for 1. and 2., and without the dot
for 3. and 4.. If none are found, it will use the default configuration.

"""
import sys
import os
import appdirs
import yaml


loaded_configuration = None


config_file = 'credrc'
dot_config_file = '.' + config_file
appname = 'cred-server'
appauthor = 'cred'

default_config = {
    'SSL': False,
    'approot': '127.0.0.1',
    'host': '*',
    'port': 5000,
    'database': {
        'type': 'sqlite3',
        'user': '',
        'password': '',
        'host': '',
        'port': '',
        'database': 'cred-server.db'
    },
    'scheduler': False,
    'schedulerPeriod': 30,
    'pingtimeout': 240
}


def locate_config_file():
    app_dirs = appdirs.AppDirs(appname, appauthor)
    if os.path.isfile(os.path.join(os.getcwd(), config_file)):
        return os.path.join(os.getcwd(), config_file)
    elif os.path.isfile(os.path.join(os.path.expanduser('~'), dot_config_file)):
        return os.path.join(os.path.expanduser('~'), dot_config_file)
    elif os.path.isfile(os.path.join(app_dirs.user_data_dir, config_file)):
        return os.path.join(app_dirs.user_data_dir, config_file)
    elif os.path.isfile(os.path.join(app_dirs.site_data_dir, config_file)):
        return os.path.join(app_dirs.site_data_dir, config_file)
    else:
        return False


def load_config_file(filename):
    try:
        config = None
        with open(filename, 'r') as f:
            config = yaml.load(f)
            print('Using configuration at {0}'.format(filename))
        if not config.keys() == default_config.keys():
            print('Invalid configuration file! (either missing or too many fields!)')
            sys.exit(1)
        return config
    except yaml.constructor.ConstructorError as e:
        print('Failed to parse configuration file! At {0}'.format(filename))
        sys.exit(1)
    except FileNotFoundError as e:
        print('Found no file at {0}'.format(filename))
        sys.exit(1)
