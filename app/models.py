import uuid
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from .ext import db

Model = db.Model
Column = db.Column


class User(Model):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(db.String, unique=True, nullable=True)
    hash = Column(db.String)
    name = Column(db.String)
    confirmed_at = Column(db.DateTime, nullable=True, default=None)
    created_at = Column(db.DateTime)
    updated_at = Column(db.DateTime)
    deleted_at = Column(db.DateTime, nullable=True, default=None)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('Password is protected')

    @password.setter
    def password(self, password):
        self.hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash, password)
