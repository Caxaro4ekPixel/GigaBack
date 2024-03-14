from app.database.models import Users


class UserAPI:
    @classmethod
    def create(cls, **kwargs):
        user = Users(**kwargs).create_user()
        return user
