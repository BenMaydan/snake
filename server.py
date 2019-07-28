from flask import Flask, request, jsonify
import pickle


# Try and except for getting the methods given
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
        try:
            data[value] = json_data[value]
        except KeyError:
            print('Value {} does not exist in json data {}'.format(value, json_data))
    return data



app = Flask(__name__)


@app.route('/test')
def test():
    """
    A test site to check if the raspberry pi server is running
    :return: Text
    """
    return "This snake game server is running!"


@app.route('/make_game', methods=['POST'])
def make_game():
    """
    Creates a game with the id to access it being the game creators hwid
    :return: game dict with information needed to draw the snakes on the screen
    """
    data = parse_json(request.get_json(force=True), ['hwid_id',])


app.run(host='0.0.0.0', port=80, debug=True)