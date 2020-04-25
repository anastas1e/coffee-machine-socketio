import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error():
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.event
def show_drinks(response):
    menu = '\n'
    for value in response['data']:
        menu += f'\n{value}'
    print(menu)


@sio.event
def show_history(response):
    if 'data' in response.keys():
        print(response['data'])
    print(response)


@sio.event
def show_additions(response):
    menu = '\n'
    for value in response['data']:
        menu += f'\n{value}'
    print(menu)


def drink_choice():
    sio.emit('show_drinks')
    drink = input("Choose: ").lower()
    addition = input('Do you want to add something to your drink? y/n: ').lower()
    if addition == 'y':
        sio.emit('show_additions')
        addit = input("Choose: ").lower()
        sio.emit('make_drink', {'drink': drink, 'addition': addit})
    elif addition == 'n':
        sio.emit('make_drink', {'drink': drink})
    else:
        print("Hey, you've entered a wrong symbol! Try again! :)")
        drink_choice()


def main():
    while True:
        choice = input('Choose an option (1 - order, 2 - show history, 3 - disconnect): ').lower()
        if choice == '1':
            drink_choice()
        elif choice == '2':
            sio.emit('show_history')
        else:
            sio.disconnect()


if __name__ == "__main__":
    sio.connect('http://localhost:5000')
    main()
    sio.wait()
