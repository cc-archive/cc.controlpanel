import os
import urllib

from fabric.api import *
from fabric.colors import yellow, green, white, red


env.roledefs['live'] = ['webadmin@a5.creativecommons.org']
env.roledefs['devel'] = ['webadmin@a7.creativecommons.org']


CCENGINE_LIVE_DIR = '/var/www/creativecommons.org/cc.engine_env/'
CCENGINE_DEVEL_DIR = '/var/www/staging.creativecommons.org/cc.engine_env/'


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


def dont_panic():
    print green(
"""
              _------_
            .'        '.  \\|||
           /            \\-_  )
     \\\\\\| ,              ,__\\\\
      (  /(  ,'-_____'-, )---'
       ||//\\ \\ """, bold=True) + white("uuuuuuu", bold=True) + green(""" //
       ',/  '.'----""", bold=True) + red(".'\\\\", bold=True) + green(""",
              '-____""", bold=True) + red("\\,/", bold=True)
    print red(
"""
             _  _ , , ___
            |O)(_)|\\|' |
           _             _
          |_) /\\ |\\ | | /  |
          |  /''\\| \\| | \\_ o""", bold=True)


def update_ccengine():
    if _on_what() == 'devel':
        ccengine_basedir = CCENGINE_DEVEL_DIR
    else:
        ccengine_basedir = CCENGINE_LIVE_DIR

    # update dependency checkouts
    if _on_what() == 'devel':
        with cd(os.path.join(ccengine_basedir, 'src/license.rdf')):
            run('git pull')
        with cd(os.path.join(ccengine_basedir, 'src/cc.license')):
            run('git pull')

    with cd(os.path.join(ccengine_basedir, 'src/cc.engine')):
        run('git pull')
        # Why not update everything, and then cc.i18n.
        # What a waste of cycles.  Oh well, it works!
        run(ccengine_basedir + 'bin/python setup.py develop -U')
        run(ccengine_basedir + 'bin/easy_install --find-links http://code.creativecommons.org/basket/ -UaZ cc.i18n')

    run('sudo /etc/init.d/apache2 reload')

    # Update license RDF
    with cd(os.path.join(ccengine_basedir, '../www/license.rdf')):
        run('git pull')


@roles('live')
def clear_cache():
    with cd('/var/www/creativecommons.org/cc.engine_env'):
        run('rm -rf cache/licenses')
