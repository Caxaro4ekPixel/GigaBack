from flask.views import MethodView
from flask import jsonify, request
from app import guard
from app.utils.validation import LoginUser, RegisterUser
from app.src.auth.utils import UserAPI
from flask_praetorian import auth_required


class BaseView(MethodView):
    decorators = [
        # auth_required,
    ]


class LoginView(MethodView):
    def post(self):
        body = LoginUser.model_validate(request.json)
        user = guard.authenticate(**body.model_dump())
        token = guard.encode_jwt_token(user)
        return jsonify({"token": token}), 200


class RegisterView(BaseView):
    def post(self):
        body = RegisterUser.model_validate(request.json)
        user = UserAPI.create(**body.model_dump())
        return jsonify({"newUser": user}), 200
