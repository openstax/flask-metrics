# -*- coding: utf-8 -*-
import time
try:
    from unittest import mock
except ImportError:
    import mock

from flask import Flask
from flask.ext.metrics import Statistician


STATSD_SETTINGS = {
    'STATSD_HOST': 'example.com',
    'STATSD_PORT': 9999,
    'STATSD_PREFIX': None,
}
#: This is the thing to be tested.
statzor = Statistician()


SUCCESS_PATH = "/path/to/enlightenment"
DOTTED_SUCCESS_PATH = SUCCESS_PATH.replace('/', '.')[1:]
ILL_PATH = "/sickly"


def make_app():
    app = Flask(__name__)

    @app.route(SUCCESS_PATH)
    def om():
        time.sleep(0.1)
        return "Om."

    @app.route(ILL_PATH)
    def achew():
        from flask import make_response, request
        status_code = int(request.args.get('status_code', 200))
        resp = make_response('', status_code)
        return resp

    return app


@mock.patch('statsd.StatsClient.timing')
def test_not_enabled(mocked_method):
    app = make_app()
    statzor.init_app(app)

    # How does one check if a pre/post-request subscriber has been registered?
    client = app.test_client()
    resp = client.get(SUCCESS_PATH)
    assert resp.status_code < 400

    assert not mocked_method.called


@mock.patch('statsd.StatsClient.timing')
def test_times_requests(mocked_method):
    app = make_app()
    app.config.update(STATSD_SETTINGS)
    statzor.init_app(app)

    # Use the test client to make a request against the application.
    client = app.test_client()
    resp = client.get(SUCCESS_PATH)
    assert resp.status_code < 400

    # The statistician timed the request and sent the metric.
    assert mocked_method.called
    assert mocked_method.call_count == 1
    (metric, value), _ = mocked_method.call_args
    expected_metric_name = 'http.get.{}.response_time' \
        .format(DOTTED_SUCCESS_PATH)
    assert metric == expected_metric_name
    assert value >= 0.1


@mock.patch('statsd.StatsClient.timing')
def test_ignores(mocked_method):
    app = make_app()
    app.config.update(STATSD_SETTINGS)
    statzor.init_app(app)

    # Use the test client to make a request against the application.
    client = app.test_client()
    for status_code in (400, 404, 500):
        resp = client.get("{}?status_code={}".format(ILL_PATH,
                                                     status_code))

    # Check the statistician *did not* send the metric.
    assert not mocked_method.called
