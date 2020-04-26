import logging
from logging.config import dictConfig

dictConfig({
        'version':    1,
        'formatters': {
                'default': {
                        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                        }
                },
        'handlers':   {
                'wsgi': {
                        'class':     'logging.StreamHandler',
                        'stream':    'ext://flask.logging.wsgi_errors_stream',
                        'formatter': 'default'
                        }
                },
        'root':       {
                'level':    'INFO',
                'handlers': ['wsgi']
                }
        })

from flask import has_request_context, request
from flask.logging import default_handler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
        )
default_handler.setFormatter(formatter)



import os

import dash
import flask
from flask.helpers import get_root_path

from config import Config


def create_app():
    server = flask.Flask(__name__)
    server.config.from_object(Config)
    register_extensions(server)
    # #logger.info('REGISTERING BLUEPRINTS...')
    register_blueprints(server)
    # #logger.info('REGISTERING DASHAPPS...')
    register_dashapps(server)
    return server

def register_dashapps(app):
    from app1.dashapp import layout
    from app1.dashapp.callbacks import register_callbacks

    dashapp1 = dash.Dash(__name__, server=app, url_base_pathname='/dash/',
                         assets_folder=os.path.join(get_root_path(__name__), 'dashapp',
                                                    'assets'))

    # logger.info('DASHAPP1 Loading')
    # dashapp.enable_dev_tools(debug=True, dev_tools_ui=True, dev_tools_props_check=True,
    #                           dev_tools_serve_dev_bundles=True,
    #                           # dev_tools_hot_reload=True,
    #                           # dev_tools_hot_reload_interval=True,
    #                           # dev_tools_hot_reload_watch_interval=True,
    #                           # dev_tools_hot_reload_max_retry=True,
    #                           dev_tools_silence_routes_logging=True,
    #                           dev_tools_prune_errors=True)

    app.config.suppress_callback_exceptions = True
    with app.app_context():
        from app1.viewmodel import DashView
        # logger.info('INITIALIZING ViewModel')
        view = DashView()
        dashapp1.title = 'CheckIt LCL Explorer'
        #logger.info('INITIALIZING Initial Layout')
        dashapp1.layout = layout(view)
        dashapp1.config['suppress_callback_exceptions'] = True
        # logger.info('Registering Callbacks')
        register_callbacks(dashapp1, view)


def register_extensions(server):
    from app1.extensions import db, migrate
    db.init_app(server)
    migrate.init_app(server,
                     db)
    #logger.info('SUCCESS Extensions Registered')


def register_blueprints(server):
    from app1.webapp import server_bp
    server.register_blueprint(server_bp)
    # logger.info('SUCCESS Blueprints Registered')
