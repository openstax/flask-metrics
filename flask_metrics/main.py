"""\
Flask extension for capturing metrics on functions and routes.
"""
from time import time

from statsd import StatsClient
from flask import current_app, request, Blueprint


class Statistician(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not app.config.get('STATSD_HOST', None):
            return  # not enabled
        app.config.setdefault('STATSD_HOST', 'localhost')
        app.config.setdefault('STATSD_PORT', 8125)
        app.config.setdefault('STATSD_PREFIX', None)
        # No connection teardown is necessary, because
        # the StatsClient does not create a connection.

        app.register_blueprint(routes_metrics_blueprint)

    @property
    def app(self):
        return current_app

    @property
    def client(self):
        host = self.app.config['STATSD_HOST']
        port = self.app.config['STATSD_PORT']
        prefix = self.app.config['STATSD_PREFIX']
        return StatsClient(host=host, port=port, prefix=prefix,
                           maxudpsize=512, ipv6=False)


statistician = Statistician()  # Singleton

routes_metrics_blueprint = Blueprint('routes_metrics', __name__)


@routes_metrics_blueprint.before_app_request
def start_timer():
    # TODO Seems like there should be a better way to register a custom
    #      request attribute, no?
    request.statclient = statistician.client

    # *clicks stopwatch*
    start = time()
    request._stats_start_time = start


@routes_metrics_blueprint.after_app_request
def stop_timer(response):
    if response.status_code >= 400:
        # Don't time 400, 404, 500, etc. responses.
        return response
    stop = time()
    delta = stop - request._stats_start_time
    dotted_path = '.'.join([x for x in request.path.split('/') if x])
    method = request.method.lower()
    metric_name = 'http.{}.{}.response_time'.format(method, dotted_path)
    request.statclient.timing(metric_name, delta)
    return response


__all__ = ('statistician', 'Statistician',)
