from flask_restx import fields, Namespace

namespace = Namespace('shared')

failed_response = namespace.model('FailResponse', {
    'error': fields.String(required=True),
    'detail': fields.String(required=False),
})
