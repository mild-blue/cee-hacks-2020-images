# pylint: disable=no-self-use
# Can not, the methods here need self due to the annotations. They are used for generating swagger which needs class.
import json
from backend.api.v1.shared_models import failed_response
from backend.auth.auth_check import require_login
from backend.auth.request_context import get_request_token
from backend.service.job_creation import create_new_job
from backend.service.job_status import get_job_status
from backend.service.result_pickup import obtain_job_result
from common.enums.job_status_enum import JobStatusEnum
from flask import Response
from flask_restx import Resource, reqparse, Namespace, fields
from uuid import UUID
from werkzeug.datastructures import FileStorage
from werkzeug.utils import redirect

# create the namespace
namespace = Namespace('job')

USER_ID = 1

# shared models
job_status_model = namespace.model('JobStatus', {
    'job_id': fields.String(
        required=True,
        description='UUID of the job in the system.',
        example='ee0ff89d-16fa-4f7b-8698-9fd9479cf4db'
    ),
    'status': fields.String(
        required=True,
        description='Status of the job in the system, '
                    'phase of the execution.',
        enum=[status.value for status in JobStatusEnum],
        example='QUEUED'
    ),
})


@namespace.route('')
class JobCreationApi(Resource):
    # input parser for files
    upload_parser = reqparse.RequestParser()
    upload_parser.add_argument('file', location='files', type=FileStorage, required=True)
    upload_parser.add_argument('metadata', location='form', type=str, required=False,
                               help='Metadata in json about the given file.')

    @namespace.doc(security='bearer')
    @namespace.expect(upload_parser)
    @namespace.response(code=200, model=job_status_model,
                        description='Queues new job for the execution.')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    @require_login()
    def post(self):
        args = self.upload_parser.parse_args()
        # TODO check max file size + check file type
        file: FileStorage = args['file']
        string_metadata: str = args.get('metadata')

        metadata = json.loads(string_metadata) if string_metadata else {}

        job_id, status = create_new_job(USER_ID, file, metadata)
        # job_id, status = create_new_job(get_request_token().user_id, file, metadata)
        return {'job_id': str(job_id), 'status': status}


@namespace.route('/status/<job_id>')
@namespace.param('job_id', 'UUID of the job.')
class JobStatusApi(Resource):

    @namespace.doc(security='bearer')
    @namespace.response(code=200, model=job_status_model,
                        description='Returns latest status of the job.')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    @require_login()
    def get(self, job_id: str):
        # TODO better handling of conversion to uuid
        status = get_job_status(USER_ID, UUID(job_id))
        # status = get_job_status(get_request_token().user_id, UUID(job_id))
        return {'job_id': str(job_id), 'status': status}


@namespace.route('/pickup/<job_id>')
@namespace.param('job_id', 'UUID of the job.')
class JobStatusApi(Resource):

    @namespace.doc(security='bearer')
    @namespace.response(code=200,
                        description='The bytes of the resulting file.')
    @namespace.response(code=302,
                        description='Redirect to the file storage where the result is located.')
    @namespace.response(code=500,
                        model=failed_response,
                        description='Unexpected error, see contents for details.')
    @namespace.produces(['text/plain', 'text/html'])
    @require_login()
    def get(self, job_id: str):
        # TODO better handling of conversion to uuid
        # file_data = obtain_job_result(get_request_token().user_id, UUID(job_id))
        file_data = obtain_job_result(USER_ID, UUID(job_id))

        if isinstance(file_data, str):
            # redirect to file storage
            return redirect(file_data)
        else:
            # decode file bytes to string and send plain text
            return Response(file_data.decode(), mimetype='text/plain')
