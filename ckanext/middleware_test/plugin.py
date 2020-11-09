import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
import sys

from flask import redirect

log = logging.getLogger(__name__)


class AuthMiddleware(object):
    def __init__(self, app, app_conf):
        self.app = app
    def __call__(self, environ, start_response):
        if 'repoze.who.identity' not in environ:
            if environ['PATH_INFO'] not in ['/', '/user/login'] \
                    and not environ['PATH_INFO'].startswith('/base') \
                    and not environ['PATH_INFO'].startswith('/api') \
                    and not environ['PATH_INFO'].startswith('/webassets') \
                    and not environ['PATH_INFO'].startswith('/images') \
                    and not environ['PATH_INFO'].startswith('/css') \
                    and not environ['PATH_INFO'].startswith('/js') \
                    and not environ['PATH_INFO'].startswith('/_debug'):
                status = "401 Unauthorized"
                headers = [('Location', '/user.login'),('Content-Length','0')]

                start_response(status, headers)
                return self.app(environ, start_response)

        return self.app(environ,start_response)


class MiddlewareTestPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IMiddleware, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')

    # IMiddleware
    def make_middleware(self, app, config):
        return AuthMiddleware(app, config)
