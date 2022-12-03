from app import database
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(database.Model):
    __tablename__ = 'users'

    id = database.Column(database.UUID, primary_key=True)
    name = database.Column(database.String(100))
    email = database.Column(database.String(70), unique=True)
    hash = database.Column(database.String(160))
    created_at = database.Column(database.DateTime)
    confirmed_at = database.Column(database.DateTime)

    def __init__(self, name: str, email: str, password_plaintext: str, user_type='User'):
        self.name = name
        self.email = email
        self.hash = self._generate_password_hash(password_plaintext)
        self.created_at = datetime.now()
        self.confirmed_at = datetime.now()
        self.user_type = user_type

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.hash, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.hash = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self.hash}>'

    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)

    def is_admin(self):
        return self.user_type == 'Admin'

    def confirm_email_address(self):
        self.confirmed_at = datetime.now()

    def remove_confirmation_email_address(self):
        self.confirmed_at = None
