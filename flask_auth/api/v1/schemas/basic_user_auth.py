"""
basic user auth schemas
"""
from flask_restx import fields
from abc import ABC


class Schema(ABC):
    def __init__(self, namespace):
        self.parser = namespace.parser()
        self.parser.add_argument('email', type=str, required=True, help="User Email Address for Authentication")


class SignUpSchema(Schema):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.parser.add_argument('password', type=str, required=True, help="User password for Authentication")
        # self.parser.add_argument('username', type=str, required=True, help="User Username for Authentication")


class SignUpSuccessResponseModel:
    def __init__(self, ns):
        self.model = ns.model('SignUpSuccessResponseModel',
                              {
                                  'message': fields.String(default="User Created Successfully",
                                                           description="Response message"),
                                  'data': fields.Nested(ns.model('UserData', {
                                      'user_id': fields.String(description="UUID of the user"),
                                      'token': fields.String(description="JWT access token"),
                                      'refresh_token': fields.String(description="JWT refresh token")
                                  }))
                              })


class LoginSuccessResponseModel:
    def __init__(self, ns):
        self.model = ns.model('SignUpSuccessResponseModel',
                              {
                                  'message': fields.String(default="User Created Successfully",
                                                           description="Response message"),
                                  'data': fields.Nested(ns.model('UserData', {
                                      'user_id': fields.String(description="UUID of the user"),
                                      'token': fields.String(description="JWT access token"),
                                      'refresh_token': fields.String(description="JWT refresh token")
                                  }))
                              })


class UnauthorizedErrorModel:
    def __init__(self, ns):
        self.model = ns.model('UnauthorizedErrorModel',
                              {
                                  'error': fields.String(default="Unauthorized"),
                                  'message': fields.String()
                              })


class ServerErrorModel:
    def __init__(self, ns):
        self.model = ns.model('ServerErrorModel',
                              {
                                  'error': fields.String(default="Internal Server Error"),
                              })


class ValidationErrorModel:
    def __init__(self, ns):
        self.model = ns.model('ValidationErrorModel',
                              {
                                  'error': fields.String(default="Bad Request"),
                                  'message': fields.String(description="Detailed explanation of the error")
                              })


class LoginSchema(Schema):
    def __init__(self, namespace):
        super().__init__(namespace)
        self.parser.add_argument('password', type=str, required=True, help="User password for Authentication")


class ForgetPWSchema(Schema):
    pass
