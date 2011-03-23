import os
import urllib

from fabric.api import *
from fabric.colors import yellow


env.roledefs['live'] = ['webadmin@a5.creativecommons.org']
env.roledefs['devel'] = ['webadmin@a7.creativecommons.org']


CCENGINE_LIVE_DIR = '/var/www/creativecommons.org/cc.engine_sanity/'
CCENGINE_DEVEL_DIR = '/var/www/staging.creativecommons.org/cc.engine_stage/'


def _on_what(host_string=None, roledefs=None):
    """
    Return which host_string this host is on.

    (Doesn't work for servers in multiple groups?)

    Args:
     - host_string: the host string; defaults to env.host_string
     - roledefs: the actual roldef groups, defaults to env.roledefs
    """
    host_string = host_string or env.host_string
    roledefs = roledefs or env.roledefs

    for group in roledefs.keys():
        if host_string in roledefs[group]:
            return group


def update_ccengine():
    if _on_what() == 'devel':
        ccengine_basedir = CCENGINE_DEVEL_DIR
    else:
        ccengine_basedir = CCENGINE_LIVE_DIR

    with cd(os.path.join(ccengine_basedir, 'cc.engine')):
        run('git pull')

    with cd(ccengine_basedir):
        run('./bin/buildout')

    run('sudo /etc/init.d/apache2 reload')

    # Update license RDF
    with cd(os.path.join(ccengine_basedir, '../www/license.rdf')):
        run('git pull')


@roles('live')
def clear_cache():
    with cd('/var/www/creativecommons.org/cc.engine_sanity'):
        run('rm -rf cache/licenses')
