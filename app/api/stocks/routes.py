from . import stocks_blueprint
from flask import (
    current_app,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    abort,
    jsonify,
)
from app.models import Stock
from app import database
from datetime import datetime


@stocks_blueprint.route("/ping")
def test():
    return "Stock Blueprint is on"


@stocks_blueprint.route("/add_stock", methods=["POST"])
def add_stock():

    # Save the form data to the database
    new_stock = Stock(
        request.form["stock_symbol"],
        request.form["number_of_shares"],
        request.form["purchase_price"],
        1,
        datetime.fromisoformat(request.form["purchase_date"]),
    )
    database.session.add(new_stock)
    database.session.commit()

    return "Success"


@stocks_blueprint.route("/stocks")
def list_stocks():

    stocks = Stock.query.order_by(Stock.id).filter_by(user_id=1).first()

    return jsonify(
        {
            "symbol": stocks.stock_symbol,
            "no of shares": stocks.number_of_shares,
            "purchase_price": stocks.purchase_price,
            "purchase_date": stocks.purchase_date,
        }
    )
