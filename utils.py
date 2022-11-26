import os
import logging
import sys


def get_env_var(name):
    if var := os.environ.get(name, False):
        return var
    else:
        logging.warning(f'Environment variable {name} not specified')
        sys.exit()
