from flask import Flask, request, jsonify
from Kitchen import *
import json
import requests
cooks = json.load(open('cooks.json', 'r'))

app = Flask(__name__)

kitchen = Kitchen(cooks, 2, 1, 'menu.json')
restaurant_data = {
    "restaurant_id" : 1,
    "name" : "McDaonald's",
    "menu_items" : len(kitchen.menu),
    "menu" : kitchen.menu,
    "rating" : 3.7
}
requests.post("https://172.0.0.1:8002/register", json=restaurant_data)
@app.route('/order', methods=['POST'])
def order():
    data = request.json
    made_food = kitchen.prepare_food(data)
    requests.post('http://127.0.0.1:3000/distribution', json=made_food)
    return "finish"

@app.route('/v2/order', methods=["POST", "GET"])
def order_v2():
    data = request.json
    made_food = kitchen.prepare_food(data)
    return jsonify(made_food)

@app.route('/v2/order/<id>', methodes = ['GET'])
def order_v2_id(id):
    if id in kitchen.prepared_foods:
        for order in kitchen.taken_orders:
            if id == order["id"]:
                order["id_ready"] = True
                order["estimated_waiting_time"] = 0
                return jsonify(order)
    else:
        for order in kitchen.taken_orders:
            if id == order["id"]:
                order["id_ready"] = False
                order["prepared_time"] = 0
                order["cooking_time"] = 0
                order["cooking_details"] = None
                return jsonify(order)

app.run(port=2000, host= '0.0.0.0')