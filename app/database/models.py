from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, relationship
from app import db, guard, login_manager
from flask_login import UserMixin
import datetime


class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    email: str = db.Column(db.String(80), unique=True, nullable=False)
    phone: str = db.Column(db.String(20), unique=True, nullable=False)
    password: str = db.Column(db.String(256), nullable=False)
    date_registration: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    is_active: bool = db.Column(db.Boolean, default=True)
    is_block: bool = db.Column(db.Boolean, default=False)

    vk_user: Mapped['VkUsers'] = relationship()
    telegram_user: Mapped['TelegramUsers'] = relationship()
    viber_user: Mapped['ViberUser'] = relationship()
    whatsapp_user: Mapped['WhatsappUser'] = relationship()
    events: Mapped['Events'] = relationship()
    user_role_list: Mapped['UserRoleList'] = relationship()

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = guard.hash_password(str(value))
            setattr(self, property, value)
        self.registered_on = datetime.datetime.now

    def __repr__(self):
        return str(self.username)

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        try:
            return self.user_role_list.split(',')
        except Exception:
            return []

    def create_user(self):
        db.session.add(self)
        db.session.commit()


class VkUsers(db.Model):
    __tablename__ = 'vk_users'

    id: int = db.Column(db.BigInteger, primary_key=True)
    user_id: int = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    vk_id: int = db.Column(db.BigInteger, nullable=False, unique=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    first_name: str = db.Column(db.String(80))
    last_name: str = db.Column(db.String(80))
    is_bot: bool = db.Column(db.Boolean, default=False)
    is_active: bool = db.Column(db.Boolean, default=True)
    is_block: bool = db.Column(db.Boolean, default=False)

    user: Mapped['Users'] = relationship(back_populates='vk_user')


class VkGroups(db.Model):
    __tablename__ = 'vk_groups'

    id: int = db.Column(db.BigInteger, primary_key=True)
    group_id: int = db.Column(db.BigInteger, unique=True, nullable=False)
    vk_user_id: int = db.Column(db.BigInteger, db.ForeignKey('vk_users.id'), nullable=False)
    name: str = db.Column(db.String(80), unique=True, nullable=False)

    vk_user: Mapped['VkUsers'] = relationship()


class TelegramUsers(db.Model):
    __tablename__ = 'telegram_users'

    id: int = db.Column(db.BigInteger, primary_key=True)
    user_id: int = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    telegram_id: int = db.Column(db.BigInteger, nullable=False, unique=True)
    username: str = db.Column(db.String(80), unique=True, nullable=False)
    phone: str = db.Column(db.String(20))
    first_name: str = db.Column(db.String(80))
    last_name: str = db.Column(db.String(80))
    is_premium: bool = db.Column(db.Boolean, default=False)
    is_bot: bool = db.Column(db.Boolean)
    is_active: bool = db.Column(db.Boolean, default=True)
    is_block: bool = db.Column(db.Boolean, default=False)

    user: Mapped['Users'] = relationship(overlaps="telegram_user")


class TelegramGroups(db.Model):
    __tablename__ = 'telegram_groups'

    id: int = db.Column(db.BigInteger, primary_key=True)
    group_id: int = db.Column(db.BigInteger, unique=True, nullable=False)
    telegram_user_id: int = db.Column(db.BigInteger, db.ForeignKey('telegram_users.id'), nullable=False)
    name: str = db.Column(db.String(80), unique=True, nullable=False)

    telegram_user: Mapped['TelegramUsers'] = relationship()


class ViberUser(db.Model):
    __tablename__ = 'viber_user'

    id: int = db.Column(db.BigInteger, primary_key=True)
    user_id: int = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    viber_id: int = db.Column(db.BigInteger, unique=True, nullable=False)
    phone: str = db.Column(db.String(20))
    first_name: str = db.Column(db.String(80))
    last_name: str = db.Column(db.String(80))
    is_bot: bool = db.Column(db.Boolean, default=False)
    is_active: bool = db.Column(db.Boolean, default=True)
    is_block: bool = db.Column(db.Boolean, default=False)

    user: Mapped['Users'] = relationship(back_populates='viber_user')


class WhatsappUser(db.Model):
    __tablename__ = 'whatsapp_user'

    id: int = db.Column(db.BigInteger, primary_key=True)
    user_id: int = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    phone: str = db.Column(db.String(20))
    first_name: str = db.Column(db.String(80))
    last_name: str = db.Column(db.String(80))
    is_bot: bool = db.Column(db.Boolean, default=False)
    is_active: bool = db.Column(db.Boolean, default=True)
    is_block: bool = db.Column(db.Boolean, default=False)

    user: Mapped['Users'] = relationship(back_populates='whatsapp_user')


class EventType(db.Model):
    __tablename__ = 'event_types'

    id: int = db.Column(db.BigInteger, primary_key=True)
    name: str = db.Column(db.String(80), unique=True, nullable=False)


class Events(db.Model):
    __tablename__ = 'events'

    id: int = db.Column(db.BigInteger, primary_key=True)
    user_id: int = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    name: str = db.Column(db.String(80), unique=True, nullable=False)
    description: str = db.Column(db.Text, nullable=False)
    event_date: datetime.datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    event_type_id: int = db.Column(db.BigInteger, db.ForeignKey('event_types.id'), nullable=False)

    user: Mapped['Users'] = relationship(back_populates='events')
    event_type: Mapped['EventType'] = relationship()


class AccessListRoles(db.Model):
    __tablename__ = 'access_list_roles'
    __table_args__ = (PrimaryKeyConstraint('privileges_id', 'role_id'),)

    privileges_id: int = db.Column(db.BigInteger, db.ForeignKey('privileges.id'))
    role_id: int = db.Column(db.BigInteger, db.ForeignKey('roles.id'))

    privileges: Mapped['Privileges'] = relationship()
    role: Mapped['Roles'] = relationship()


class Roles(db.Model):
    __tablename__ = 'roles'

    id: int = db.Column(db.BigInteger, primary_key=True)
    name: str = db.Column(db.String())
    ru_name: str = db.Column(db.String())
    is_active: bool = db.Column(db.Boolean, default=True)


class UserRoleList(db.Model):
    __tablename__ = 'user_role_list'
    __table_args__ = (PrimaryKeyConstraint('user_id', 'role_id'),)

    user_id: int = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    role_id: int = db.Column(db.BigInteger, db.ForeignKey('roles.id'))

    user: Mapped['Users'] = relationship(back_populates='user_role_list')
    role: Mapped['Roles'] = relationship()


class Privileges(db.Model):
    __tablename__ = 'privileges'

    id: int = db.Column(db.BigInteger, primary_key=True)
    role_id: int = db.Column(db.BigInteger, db.ForeignKey('roles.id'))
    name: str = db.Column(db.String())
    ru_name: str = db.Column(db.String())
    level: int = db.Column(db.Integer)
    is_active: bool = db.Column(db.Boolean, default=True)

    role: Mapped['Roles'] = relationship()


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
