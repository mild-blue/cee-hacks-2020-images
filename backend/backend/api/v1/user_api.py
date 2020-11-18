# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.
import logging
from typing import Tuple

from flask import request, Response
from flask_restx import Resource, fields, Namespace

from backend.api.v1.shared_models import failed_response
from backend.auth.auth_check import require_login, require_admin
from backend.auth.auth_management import register_user
from backend.auth.login import credentials_login, refresh_token
from common.enums.app_user_role import AppUserRole

logger = logging.getLogger(__name__)

# create the namespace
namespace = Namespace('user')

# shared models
login_success = namespace.model('LoginSuccessResponse', {
    'auth_token': fields.String(required=True,
                                description='Token that should be used for authentication.'),
})


@namespace.route('/login')
class LoginApi(Resource):
    login_input_model = namespace.model('UserLogin', {
        'username': fields.String(required=True, description='Username for the user login.'),
        'password': fields.String(required=True, description='User\'s password.')
    })

    @namespace.doc(body=login_input_model)
    @namespace.response(code=200, model=login_success,
                        description='Login successful. JWT generated. User must attach the token to every request '
                                    'in the "Authorization" header with the prefix "Bearer". Example: '
                                    '"Authorization: Bearer some_token", where some_token is the token received '
                                    'in the response.')
    @namespace.response(code=400, model=failed_response, description='Wrong data format.')
    @namespace.response(code=401, model=failed_response, description='Authentication failed.')
    @namespace.response(code=500, model=failed_response, description='Unexpected error, see contents for details.')
    def post(self):
        post_data = request.get_json()
        auth_response = credentials_login(username=post_data['username'], password=post_data['password'])
        return _respond_token(auth_response)


@namespace.route('/refresh-token')
class RefreshTokenApi(Resource):

    @namespace.doc(security='bearer')
    @namespace.response(code=200, model=login_success, description='Token successfully refreshed.')
    @namespace.response(code=400, model=failed_response, description='Wrong data format.')
    @namespace.response(code=401, model=failed_response, description='Authentication failed.')
    @namespace.response(code=500, model=failed_response, description='Unexpected error, see contents for details.')
    @require_login()
    def get(self):
        return _respond_token(refresh_token())


@namespace.route('/register', methods=['POST'])
class RegistrationApi(Resource):
    registration_model = namespace.model('UserRegistration', dict(
        username=fields.String(required=True, description='Username used for authentication.'),
        password=fields.String(required=True, description='User\'s password.'),
        role=fields.String(required=True, enum=[role.name for role in AppUserRole], description='User\'s role.'),
    ))

    @namespace.doc(body=registration_model, security='bearer')
    @namespace.response(code=200, description='User registered successfully.')
    @namespace.response(code=400, model=failed_response, description='Wrong data format.')
    @namespace.response(code=401, model=failed_response, description='Authentication failed.')
    @namespace.response(code=403, model=failed_response,
                        description='Access denied. You do not have rights to access this endpoint.')
    @namespace.response(code=500, model=failed_response, description='Unexpected error, see contents for details.')
    # @require_admin() TODO: Commented just temporary
    def post(self):
        post_data = request.get_json()
        register_user(username=post_data['username'],
                      password=post_data['password'],
                      role=AppUserRole(post_data['role']))
        return Response(status=200)


def _respond_token(token: str) -> Tuple[dict, int]:
    return {'auth_token': token}, 200
