from fabric.api import *
import urllib

env.roledefs['live'] = ['webadmin@a5.creativecommons.org']
env.roledefs['devel'] = ['webadmin@a7.creativecommons.org']

def test_live_devel():
    if env.host_string in env.roledefs['live']:
        print "%s is in live" % env.host
    elif env.host_string in env.roledefs['devel']:
        print "%s is in devel" % env.host

def update_ccengine(clear_cache=False):
    with cd('/var/www/creativecommons.org/cc.engine_sanity/cc.engine'):
        run('git pull')

    with cd('/var/www/creativecommons.org/cc.engine_sanity'):
        run('./bin/buildout')
    run('sudo /etc/init.d/apache2 reload')
