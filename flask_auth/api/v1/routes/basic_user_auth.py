import os
from flask_restx import Resource, Namespace, fields, abort, marshal
from werkzeug.exceptions import BadRequest
from flask import make_response, jsonify
from .routes import basic_user_ns
from flask_auth.api.v1.schemas.basic_user_auth import SignUpSchema,  SignUpSuccessResponseModel, LoginSchema, ForgetPWSchema, UnauthorizedErrorModel, ServerErrorModel, ValidationErrorModel, LoginSuccessResponseModel
from shared.services.user import create_user, get_user_by_email, send_account_activation_mail
from shared.services.token import generate_token, generate_refresh_token
from shared.services.pw_bcrypt import check_pw
from db.engine import session_manager
from db.model.user import Users


@basic_user_ns.route('/signup')
class BasicUserSignUp(Resource):
    parser = SignUpSchema(basic_user_ns).parser

    @basic_user_ns.expect(parser)
    @basic_user_ns.marshal_with(SignUpSuccessResponseModel(basic_user_ns).model, as_list=True)
    @basic_user_ns.response(500, 'Internal Server Error', ServerErrorModel(basic_user_ns).model)
    @basic_user_ns.response(400, 'Validation Error', ValidationErrorModel(basic_user_ns).model)
    def post(self):
        args = self.parser.parse_args()

        result = get_user_by_email(args.get('email'))
        if result:
            e = BadRequest('My custom message')
            e.data = {'error': 'Bad Request', 'message': 'Email already exists'}
            raise e

        elif result is False:
            abort(500, 'Internal Server Error')

        user = create_user(args)
        token = generate_token(user_id=str(user.get_id()), token_key=os.getenv('APP_TOKEN_KEY'))
        refresh_token = generate_refresh_token(user_id=str(user.get_id()), refresh_token_key=os.getenv('APP_REFRESH_TOKEN_KEY'))

        response = {
            "message": "User Created Successfully",
            "data": {
                "user_id": str(user.get_id()),
                "token": token,
                "refresh_token": refresh_token
            }
        }
        return response, 201


@basic_user_ns.route('/login')
class BasicUserLogin(Resource):
    parser = LoginSchema(basic_user_ns).parser

    @basic_user_ns.expect(parser)
    @basic_user_ns.marshal_with(LoginSuccessResponseModel(basic_user_ns).model, as_list=True)
    @basic_user_ns.response(500, 'Internal Server Error', ServerErrorModel(basic_user_ns).model)
    @basic_user_ns.response(400, 'Validation Error', ValidationErrorModel(basic_user_ns).model)
    def post(self):
        args = self.parser.parse_args()
        user_email = args.get('email')
        user_pw = args.get('password')
        user = get_user_by_email(user_email)
        if user:
            if check_pw(user_pw, user.password_hash):
                token = generate_token(user_id=str(user.get_id()), token_key=os.getenv('APP_TOKEN_KEY'))
                refresh_token = generate_refresh_token(user_id=str(user.get_id()), refresh_token_key=os.getenv('APP_REFRESH_TOKEN_KEY'))

                response = {
                    "message": "User Logged In Successfully",
                    "data": {
                        "user_id": str(user.get_id()),
                        "token": token,
                        "refresh_token": refresh_token
                    }
                }
                return response, 201

            else:
                e = BadRequest('My custom message')
                e.data = {'error': 'Bad Request', 'message': 'Wrong Password'}
                raise e
        else:
            e = BadRequest('My custom message')
            e.data = {'error': 'Bad Request', 'message': 'User does not exist'}
            raise e


@basic_user_ns.route('/forget_pw')
class BasicUserForgetPW(Resource):
    parser = ForgetPWSchema(basic_user_ns).parser

    @basic_user_ns.expect(parser)
    def post(self):
        args = self.parser.parse_args()
        return {
            "type": 'forget_pw',
        }.update(args), 202


@basic_user_ns.route('/change_pw/token')
class BasicUserChangePW(Resource):
    @staticmethod
    @basic_user_ns.doc(security='Bearer Auth')
    def get(token: str):
        return {
            'type': 'change_pw',
            'token': token
        }, 200


@basic_user_ns.route('/activate_account/<token>')
class BasicUserActivateAccount(Resource):
    @staticmethod
    def get(token: str):
        pass


@basic_user_ns.route('/init_account_activation/<email>')
class BasicUserActivateAccountEmail(Resource):
    @staticmethod
    def get(email: str):
        user = get_user_by_email(email)
        if user is None:
            e = BadRequest('My custom message')
            e.data = {'error': 'Bad Request', 'message': f'User with Email[{email}] not found'}
            raise e
        elif user is False:
            abort(500, 'Internal Server Error')
        send_account_activation_mail(email)
        return {
            "message": "Activation Mail Sent Successfully",
        }



@basic_user_ns.route('/users')
class GetUsers(Resource):
    @staticmethod
    def get():
        users = []
        with session_manager() as session:
            results = session.query(Users).all()
            for result in results:
                users.append(
                    {
                        "email": result.email,
                        "id": str(result.get_id()),
                        "is_verified": result.is_verified
                    }
                )
        return users, 200
