# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.
import logging

from flask import jsonify
from flask_restx import Resource, Namespace, fields

from backend.api.v1.shared_models import failed_response
from backend.configuration.application_configuration import get_application_configuration, ApplicationEnvironment

logger = logging.getLogger(__name__)

namespace = Namespace('service')


@namespace.route('/status')
class Status(Resource):
    model = namespace.model('ServiceStatus', {
        'status': fields.String(required=True,
                                description='Indication of service\'s health.',
                                enum=['OK', 'Failing']),
    })

    @namespace.response(code=200,
                        model=model,
                        description='Returns ok if the service is healthy.')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    def get(self):
        return {'status': 'ok'}


@namespace.route('/version')
class Version(Resource):
    model = namespace.model('Version', {
        'version': fields.String(required=True, description='Version of the running code.'),
        'environment': fields.String(required=True,
                                     enum=[env.value for env in ApplicationEnvironment],
                                     description='Environment the code was build for.')
    })

    @namespace.response(code=200,
                        model=model,
                        description='Returns version of the code')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    def get(self):
        conf = get_application_configuration()
        logger.debug(f'Application version: {conf.code_version} in environment {conf.environment}.')
        return jsonify({'version': conf.code_version, 'environment': conf.environment})
