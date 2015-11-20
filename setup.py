"""Flask Metrics
   ~~~~~~~~~~~~~

   Provides an interface for capturing metrics (via StatsD).

   :copyright:  (c) 2015-2016 Rice University.
   :author: pumazi

"""
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def read_requirements(f):
    reqs = []
    with open(f, "r") as h:
        reqs = [req.split('#', 1)[0].strip() for req in h]
        reqs = [req for req in reqs if req]
    return reqs


install_requires = read_requirements('requirements.txt')
features = []
extras_require = {x: read_requirements('requirements-{x}.txt'.format(x=x))
                  for x in features}

setup(
    name='flask-metrics',
    version='1.0.0',
    author='Michael Mulich',
    author_email='michael.mulich@gmail.com',
    license='AGPL, See also LICENSE.txt',
    long_description=open('README.rst').read(),
    install_requires=install_requires,
    extras_require=extras_require,
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    packages=find_packages(),
    include_package_data=True
)
