=======================
Flask Metrics Extension
=======================

Provides an proxy for the
`statsd.StatsClient <https://statsd.readthedocs.org/en/latest/reference.html#statsclient>`_
and a tranparent component to time requests.

All routes that result in responses > HTTP 400 will be timed under the metric name:
``[STATSD_PREFIX.]http.<method>.<dotted-path>.response_time``. Where the ``STATSD_PREFIX`` setting (see installation) is optional, but highly recommended; ``method`` is the HTTP verb (e.g. get, post); ``dotted-path`` is the path name in dotted form (e.g. ``/foo/bar`` becomes ``foo.bar``).

Installation
------------

Install from github::

    git clone https://github.com/openstax/flask-metrics.git
    pip install ./flask-metrics

Configure in your application::

    from flask import Flask
    from flask.ext.metrics import statistician

    app = Flask(__name__)

    # required setting to enable the extension
    app.config['STATSD_HOST'] = 'localhost'
    # optional...
    app.config['STATSD_PORT'] = 8125  # default
    app.config['STATSD_PORT'] = 'myapp'  # default: None

    statistician.init_app(app)

If the ``STATSD_HOST`` is assigned, the request/response timer metric will be enabled.

Test
----

Install and use py.test::

    pip install pytest
    cd flask-metrics
    py.test

License
-------

This software is subject to the provisions of the GNU Affero General
Public License Version 3.0 (AGPL). See license.txt for details.
Copyright (c) 2015 Rice University
