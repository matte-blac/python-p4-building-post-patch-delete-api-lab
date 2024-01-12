#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def bakery_by_id(id):
    # get the bakery by id
    bakery = db.session.get(Bakery, id)

    # if the bakery doesn't exist, return a 404 error
    if bakery is None:
        return jsonify({'error': 'Bakery not found'}), 404
    
    # get the new name from the form data
    new_name = request.form.get('name')

    # update the bakery's name
    bakery.name = new_name

    # commit the changes to the database
    db.session.commit()

    # return the updated bakery's data as JSON
    return jsonify(bakery.to_dict()), 200

    # bakery = Bakery.query.filter_by(id=id).first()
    # bakery_serialized = bakery.to_dict()
    # return make_response ( bakery_serialized, 200 s )

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    # get data from the form
    name = request.form.get('name')
    price = request.form.get('price')

    # create a new BakedGood object
    new_baked_good = BakedGood(name=name, price=price)

    # add the new baked good to the database
    db.session.add(new_baked_good)
    db.session.commit()

    #return the new baked good's data as JSON
    return jsonify(new_baked_good.to_dict()), 201

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    # get the baked by id
    baked_good = db.session.get(BakedGood, id)

    # if the baked good doesn't exist, return a 404 error
    if baked_good is None:
        return jsonify({'error': 'Baked good not found'}), 404
    
    # delete the baked good from the database
    db.session.delete(baked_good)
    db.session.commit()

    # return a confirmation message
    return jsonify({'message': 'Baked good successfully deleted'}), 200

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)