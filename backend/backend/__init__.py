import pathlib

import os

from common.logger import init_logging
from dotenv import load_dotenv
from flask import Flask, redirect, send_from_directory, request
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from backend.api.v1 import API_VERSION as V1
from backend.api.v1.job_api import namespace as job_namespace
from backend.api.v1.service_api import namespace as service_namespace
from backend.api.v1.shared_models import namespace as shared_models_namespace
from backend.api.v1.user_api import namespace as user_namespace
from backend.configuration.application_configuration import ApplicationConfiguration, get_application_configuration
from common.db.database import get_db_session, init_db, migrate_db, build_db_connection_string
from common.dto.database_configuration import DatabaseConfiguration

_SWAGGER_URL = '/doc/'


def create_app() -> Flask:
    init_logging()
    app = Flask(__name__)
    # fix for https swagger - see https://github.com/python-restx/flask-restx/issues/58
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)

    def load_local_development_config():
        env_file = os.path.join(pathlib.Path().absolute(), '../.env')
        if os.path.exists(env_file):
            load_dotenv(dotenv_path=env_file, verbose=True)
            app.config['IS_LOCAL_DEV'] = True

    def connect_to_database(conf: ApplicationConfiguration):
        # connect to the database
        # docs https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/
        init_db(DatabaseConfiguration(
            postgres_user=conf.postgres_user,
            postgres_password=conf.postgres_password,
            postgres_url=conf.postgres_url,
            postgres_db=conf.postgres_db
        ))
        # process the migrations
        migrate_db(build_db_connection_string(
            postgres_user=conf.postgres_user,
            postgres_password=conf.postgres_password,
            postgres_url=conf.postgres_url,
            postgres_db=conf.postgres_db
        ))

    def configure_apis():
        authorizations = {
            'bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            }
        }

        api = Api(
            doc=_SWAGGER_URL,
            version='0.1',
            title='CEE Hacks 2020 API',
            authorizations=authorizations,
        )
        api.init_app(app)
        api.add_namespace(shared_models_namespace)
        api.add_namespace(job_namespace, path=f'{V1}/job')
        api.add_namespace(service_namespace, path=f'{V1}/service')
        api.add_namespace(user_namespace, path=f'{V1}/user')

    # def init_default_routes():
    #     # pylint: disable=unused-variable
    #     @app.route('/')
    #     def redirect_to_swagger():
    #         return redirect(_SWAGGER_URL, code=302)

    def configure_data_upload(conf: ApplicationConfiguration):
        app.config['MAX_CONTENT_LENGTH'] = conf.max_file_size_mb * 1024 * 1024

    def configure_context_hooks():
        # close session when the request is processed
        # https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            session = get_db_session()
            if session:
                session.remove()

    def register_static_proxy():
        # serving main html which then asks for all javascript
        @app.route('/')
        def index_html():
            return send_from_directory('frontend/dist/frontend', 'index.html')

        # used only if the there's no other endpoint registered
        # we need it to load static resources for the frontend
        @app.route('/<path:path>', methods=['GET'])
        def static_proxy(path):
            return send_from_directory('../frontend/dist/frontend', path)

    def enable_cors():
        @app.after_request
        def add_headers(response):
            allowed_origins = {
                '*'  # proxy on staging, support for swagger
            }
            origin = request.headers.get('origin')
            if origin in allowed_origins:
                response.headers.add('Access-Control-Allow-Origin', origin)
                response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
                response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT')
            return response

    with app.app_context():
        # load configuration
        load_local_development_config()
        conf = get_application_configuration()
        # initialize database engine
        connect_to_database(conf)
        # configure context lifetime
        configure_context_hooks()
        # configure restrictions for file upload
        configure_data_upload(conf)
        # register basic routes
        # init_default_routes()
        register_static_proxy()
        # finish configuration
        configure_apis()
        return app
