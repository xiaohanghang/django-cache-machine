"""
Creating standalone Django apps is a PITA because you're not in a project, so
you don't have a settings.py file.  I can never remember to define
DJANGO_SETTINGS_MODULE, so I run these commands which get the right env
automatically.
"""
import os
import sys

from subprocess import call, check_output

NAME = os.path.basename(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(__file__))

os.environ['PYTHONPATH'] = os.pathsep.join([ROOT,
                                            os.path.join(ROOT, 'examples')])

SETTINGS = (
    'locmem_settings',
    'settings',
    'memcache_byid',
    'custom_backend',
    'redis_settings',
    'redis_byid',
)


def main():
    results = []
    django_admin = check_output(['which', 'django-admin.py']).strip()
    for i, settings in enumerate(SETTINGS):
        print('Running tests for: %s' % settings)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'cache_machine.%s' % settings
        # append to the existing coverage data for all but the first run
        if i > 0:
            coverage_cmd = ['coverage', 'run', '--append', django_admin, 'test']
        else:
            coverage_cmd = ['coverage', 'run', django_admin, 'test']
        results.append(call(coverage_cmd))
        results.append(call(['coverage', 'report', '-m', '--fail-under', '70']))
    sys.exit(any(results) and 1 or 0)


if __name__ == "__main__":
    main()
