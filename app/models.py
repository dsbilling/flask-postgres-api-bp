from app import database
from flask import current_app
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import requests

################
#### Models ####
################

class Stock(database.Model):

    __tablename__ = 'stocks'

    id = database.Column(database.Integer, primary_key=True)
    stock_symbol = database.Column(database.String, nullable=False)
    number_of_shares = database.Column(database.Integer, nullable=False)
    purchase_price = database.Column(database.Integer, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    purchase_date = database.Column(database.DateTime)
    current_price = database.Column(database.Integer)
    current_price_date = database.Column(database.DateTime)
    position_value = database.Column(database.Integer)

    def __init__(self, stock_symbol: str, number_of_shares: str, purchase_price: str,
                 user_id: int, purchase_date=None):
        self.stock_symbol = stock_symbol
        self.number_of_shares = int(number_of_shares)
        self.purchase_price = int(float(purchase_price) * 100)
        self.user_id = user_id
        self.purchase_date = purchase_date
        self.current_price = 0
        self.current_price_date = None
        self.position_value = 0

    def __repr__(self):
        return f'{self.stock_symbol} - {self.number_of_shares} shares purchased at ${self.purchase_price / 100}'


class User(database.Model):

    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(100))
    email = database.Column(database.String(70), unique = True)
    password_hashed = database.Column(database.String(160))
    registered_on = database.Column(database.DateTime)
    email_confirmation_sent_on = database.Column(database.DateTime)
    email_confirmed = database.Column(database.Boolean, default=False)
    email_confirmed_on = database.Column(database.DateTime)
    stocks = database.relationship('Stock', backref='user', lazy='dynamic')
    user_type = database.Column(database.String(10), default='User')
    watchstocks = database.relationship('WatchStock', backref='user', lazy='dynamic')

    def __init__(self, name:str, email: str, password_plaintext: str, user_type='User'):

        self.name = name
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()
        self.email_confirmation_sent_on = datetime.now()
        self.email_confirmed = False
        self.email_confirmed_on = None
        self.user_type = user_type

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self.password_hashed}>'

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
        self.email_confirmed = True
        self.email_confirmed_on = datetime.now()

    def unconfirm_email_address(self):
        self.email_confirmed = False
        self.email_confirmed_on = None


class WatchStock(database.Model):

    __tablename__ = 'watchstocks'

    id = database.Column(database.Integer, primary_key=True)
    stock_symbol = database.Column(database.String, nullable=False)
    company_name = database.Column(database.String)
    current_share_price = database.Column(database.Integer)
    current_share_price_date = database.Column(database.DateTime)
    fiftytwo_week_low = database.Column(database.Integer)
    fiftytwo_week_high = database.Column(database.Integer)
    market_cap = database.Column(database.String)
    dividend_per_share = database.Column(database.Integer)
    pe_ratio = database.Column(database.Integer)
    peg_ratio = database.Column(database.Integer)
    profit_margin = database.Column(database.Integer)
    beta = database.Column(database.Integer)
    price_to_book_ratio = database.Column(database.Integer)
    stock_data_date = database.Column(database.DateTime)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'))

    def __init__(self, stock_symbol: str, user_id: str):
        self.stock_symbol = stock_symbol
        self.company_name = None
        self.current_share_price = 0
        self.current_share_price_date = None
        self.fiftytwo_week_low = 0
        self.fiftytwo_week_high = 0
        self.market_cap = None
        self.dividend_per_share = 0
        self.pe_ratio = 0
        self.peg_ratio = 0
        self.profit_margin = 0
        self.beta = 0
        self.price_to_book_ratio = 0
        self.stock_data_date = None
        self.user_id = user_id

    def __repr__(self):
        return f'{self.stock_symbol}'