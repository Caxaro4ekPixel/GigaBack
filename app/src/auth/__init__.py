from flask import Blueprint

auth = Blueprint(
    'auth_blueprint',
    __name__,
    url_prefix='',
)
