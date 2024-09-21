from flask_restx import Api
from flask import Flask


class CreateApp(object):
    def __init__(self, endpoints_update=""):
        self.app = Flask(__name__)
        self.api = Api(app=self.app, version='1.0.0', title='AuthX Flask REST-API', doc='/docs')
        self.endpoints_update = endpoints_update
        self.setup_endpoints()

    def setup_endpoints(self):
        for namespace, path in self.endpoints_update:
            self.api.add_namespace(namespace, path)
        self.api.authorizations = {
            'Bearer Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer <token>"'
            }
        }
