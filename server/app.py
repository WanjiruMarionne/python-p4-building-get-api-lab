#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route("/bakeries")
def all_bakeries():
    bakeries_dict = [bakery.to_dict(rules=("-baked_goods",)) for bakery in Bakery.query.all()]

    return make_response(bakeries_dict, 200)

@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery:
        return make_response(bakery.to_dict(), 200)
    else:
        return make_response({"errors": "Bakery not found"}, 404)
    
@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc("price")).all()
    baked_goods_dict = [baked_good.to_dict(rules=("-bakery",)) for baked_good in baked_goods]

    return make_response(baked_goods_dict, 200)

@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    most_expensive_baked_good = BakedGood.query.order_by(desc("price")).limit(1).first()
    return make_response(most_expensive_baked_good.to_dict(), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
