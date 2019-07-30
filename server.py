from flask import Flask, request, jsonify
import pickle


# Try and except to confirm arguments exist given
def parse_json(json_data, required):
    """
    Does a try and except to parse through the json
    Instead of crashing the server, this will return all of the data needed
    :param json_data: Json data passed by the request maker
    :param required: All of the required keys in the json data
    :return: dictionary required[key]:json_data[key]
    """
    data = {}
    for value in required:
        print(value)
        try:
            data[value] = json_data[value]
        except KeyError:
            print('Value {} does not exist in json data {}'.format(value, json_data))
    return data

# Function to modify file contents
def file(name, mode, dump=None):
    """
    Either accesses and returns the file contents or modifies the file
    :param name: The name of the file
    :param mode: The mode to open the file in (rb, wb)
    :param dump: What to dump in the file if the mode is wb
    :return: The file contents
    """
    mapping = {'rb': lambda: pickle.load(name, NameError), 'wb': lambda: pickle.dump(dump, name)}


# Makes the flask app
app = Flask(__name__)


@app.route('/test')
def test():
    """
    A test site to check if the raspberry pi server is running
    :return: Text
    """
    return "This snake game server is running!"


@app.route('/create', methods=['POST'])
def make_game():
    """
    Creates a game with the id to access it being the game creators hwid
    :return: game dict with information needed to draw the snakes on the screen
    """
    data = parse_json(request.get_json(force=True), ['hwid', 'name', 'intensity'])


@app.route('/join', methods=['POST'])
def join_game():
    """
    Joins the snake game
    :return:
    """
    data = parse_json(request.get_json(force=True), ['hwid', 'name'])
    file_data = file()


@app.route('/printable', methods=['GET'])
def printable():
    """
    :return: list of snake coordinate values that can be printed to the screen
    """



app.run(host='0.0.0.0', port=80, debug=True)