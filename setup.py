#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import shutil
from minify import command as minify
from distutils.cmd import Command
from subprocess import call

if sys.version_info < (3, 2):
    print("ApiDoc requires Python 3.2 or later")
    raise SystemExit(1)

from setuptools.command.test import test

from setuptools import setup, find_packages

from apidoc import __version__


class ApiDocTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

class Resource(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        resource_dir = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                'apidoc',
                'template',
                'resource'
            )
        )

        resource_src_dir = os.path.realpath(os.path.join(resource_dir, 'src'))
        resource_src_js_dir = os.path.realpath(os.path.join(resource_src_dir, 'js'))
        resource_src_css_dir = os.path.realpath(os.path.join(resource_src_dir, 'css'))
        resource_src_less_dir = os.path.realpath(os.path.join(resource_src_dir, 'less'))
        resource_js_dir = os.path.realpath(os.path.join(resource_dir, 'js'))
        resource_css_dir = os.path.realpath(os.path.join(resource_dir, 'css'))

        os.system("wget --post-data='css=%s&js=%s' -O '/tmp/bootstrap.zip' %s" % (
            '["reset.less","scaffolding.less","grid.less","layouts.less","type.less","code.less","tables.less","forms.less","navs.less","navbar.less","tooltip.less","popovers.less","modals.less","wells.less","close.less","utilities.less","component-animations.less","responsive-utilities.less","responsive-767px-max.less","responsive-768px-979px.less","responsive-1200px-min.less","responsive-navbar.less"]',
            '["bootstrap-transition.js","bootstrap-modal.js","bootstrap-scrollspy.js","bootstrap-tooltip.js","bootstrap-popover.js","bootstrap-affix.js"]',
            'http://bootstrap.herokuapp.com'
        ))

        assert os.path.exists('/tmp/bootstrap.zip'), 'Downloaded bootstrap zip not found'

        try:
            os.system('unzip /tmp/bootstrap.zip -d /tmp/apidoc-bootstrap')

            shutil.move('/tmp/apidoc-bootstrap/js/bootstrap.min.js', '%s/bootstrap.min.js' % resource_src_js_dir)
            shutil.move('/tmp/apidoc-bootstrap/css/bootstrap.min.css', '%s/bootstrap.min.css' % resource_src_css_dir)
        finally:
            os.remove('/tmp/bootstrap.zip')
            shutil.rmtree('/tmp/apidoc-bootstrap')

        os.system('wget -O "%s" "%s"' % ('%s/jquery.min.js' % resource_src_js_dir, 'http://code.jquery.com/jquery-2.0.3.min.js'))
        assert os.path.exists('%s/mousetrap.min.js' % resource_src_js_dir), 'Downloaded jquery file not found'

        os.system('wget -O "%s" "%s"' % ('%s/mousetrap.min.js' % resource_src_js_dir, 'http://cdn.craig.is/js/mousetrap/mousetrap.min.js'))
        assert os.path.exists('%s/mousetrap.min.js' % resource_src_js_dir), 'Downloaded mousetrap file not found'

        os.system('lessc -x "%s/apidoc.less" "%s/apidoc.css"' % (resource_src_less_dir, resource_src_css_dir))

        for folder in  [resource_css_dir, resource_js_dir]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        os.system('/usr/bin/env python3 %s minify_css --sources "%s/*.css %s/font.css" --output "%s/combined.css"' % (__file__, resource_src_css_dir, resource_css_dir, resource_css_dir))
        assert os.path.exists('%s/combined.css' % resource_css_dir), 'Combined css file not found'

        os.system('/usr/bin/env python3 %s minify_css --sources "%s/*.css %s/font-embedded.css" --output "%s/combined-embedded.css"' % (__file__, resource_src_css_dir, resource_css_dir, resource_css_dir))
        assert os.path.exists('%s/combined-embedded.css' % resource_css_dir), 'Combined embedded css file not found'

        os.system('/usr/bin/env python3 %s minify_js --sources "%s/*.js" --output "%s/combined.js"' % (__file__, resource_src_js_dir, resource_js_dir))
        assert os.path.exists('%s/combined.js' % resource_js_dir), 'Combined js file not found'



if (3, 2) <= sys.version_info < (3, 3):
    requirements = ['Jinja2 == 2.6', 'PyYAML', 'jsonschema']
else:
    requirements = ['Jinja2', 'PyYAML', 'jsonschema']


setup(
    name='ApiDoc',
    version=__version__,
    description='Api Documentation Generator',
    long_description='''About
=====

ApiDoc is a documentation generator designe for API built with Python.

Full documentation available on https://apidoc.rtfd.org.

Installation
============

$ pip3 install apidoc''',
    author='Jérémy Derussé',
    author_email='jeremy.derusse@sfr.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
    ],
    platforms=['Any'],
    license='GPLv3+',
    url='http://solutionscloud.github.io/apidoc/',
    packages=find_packages(exclude=['tests', 'tests.*', 'example', 'example.*', 'docs', 'docs.*']),
    entry_points={
        'console_scripts': [
            'apidoc-analyse = apidoc.command.analyse:main',
            'apidoc-render = apidoc.command.render:main',
            'apidoc-watch = apidoc.command.watch:main',
        ],
    },
    include_package_data=True,
    package_data={'apidoc': [
        'template/*.html',
        'template/helper/*.html',
        'template/partial/*.html',
        'template/layout/*.html',
        'template/resource/css/*.css',
        'template/resource/js/*.js',
        'template/resource/font/*',
        'datas/schemas/*.yml',
        'command/logging.yml',
    ]},
    install_requires=requirements,
    tests_require=['mock', 'pytest'],
    cmdclass={
        'test': ApiDocTest,
        'resources': Resource,
        'minify_js': minify.minify_js,
        'minify_css': minify.minify_css
    }
)
