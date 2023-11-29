
from flask import Flask, request, redirect
from flask import jsonify
from dotenv import load_dotenv
from actions.openai import add_thread_message, create_run, create_thread, get_thread_last_message, retrieve_run




from api.hubspot import hubspot
from api.messenger import messenger
from api.chat import chat
import os

from tools.openai import create_run_and_get_last_message

load_dotenv()

app = Flask(__name__)

app.register_blueprint(hubspot, url_prefix='/hubspot')
app.register_blueprint(messenger, url_prefix='/messenger')
app.register_blueprint(chat, url_prefix='/chat')


assistant_id = os.getenv('VITALITY_RX_OPENAI_ASSISTANT_ID')


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'GET request received!'})

@app.route('/start', methods=['POST'])
def start():
    create_thread_response = create_thread()
    create_thread_response_json = create_thread_response.json
    thread_id = create_thread_response_json['id']

    add_thread_message(thread_id, "hi")

    last_message = create_run_and_get_last_message(thread_id,assistant_id)

    return last_message




if __name__ == '__main__':
    app.run(host='localhost' ,debug=True, port=5001)
