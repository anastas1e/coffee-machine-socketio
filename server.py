import socketio
import eventlet
import datetime

sio = socketio.Server()
app = socketio.WSGIApp(sio)

drinks = {"cappuccino": 20, "americano": 15, "latte": 10, "frappe": 5, "macchiato": 2}
adds = {"sugar": 30, "caramel": 20, "cinnamon": 10, "vanilla extract": 2}
orders = {}


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
def show_history(sid):
    sio.emit('show_history', {'data': orders})


@sio.event
def show_drinks(sid):
    sio.emit('show_drinks', {'data': drinks})


@sio.event
def show_additions(sid):
    sio.emit('show_additions', {'data': adds})


@sio.event
def make_drink(sid, data):
    response = check(data)
    if "Error" in response.keys():
        sio.emit('show_history', response)
    if 'OK' in response:
        if 'addition' in data:
            adds[data['addition']] -= 1
        drinks[data['drink']] -= 1
        order = {"Time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Description": data}
        orders[sid] = order

    sio.emit('show_history', response)


def check(data):
    if data['drink'] not in drinks.keys():
        return {"Error": 404, "Description": "Not found. You have entered a non-existent drink"}
    elif drinks[data['drink']] == 0:
        return {"Error": 403, "Description": "Forbidden. This drink is out of stock."}
    elif 'addition' in data:
        if data['addition'] not in adds.keys():
            return {"Error": 404, "Description": "Not found. You have entered a non-existent addition"}
        elif adds[data['addition']] == 0:
            return {"Error": 403, "Description": "Forbidden. This addition is out of stock."}
        else:
            return {"OK": 201, "Description": f"{data['drink']} with {data['addition']} is preparing.."}
    elif 'addition' not in data:
        return {"OK": 201, "Description": f"{data['drink']} is preparing.."}


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
