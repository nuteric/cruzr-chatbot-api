
from flask import Flask
from flask import jsonify
from dotenv import load_dotenv




from api.hubspot import hubspot
from api.messenger import messenger
from api.chat import chat
import os

from tools.openai import create_run_and_get_last_message

load_dotenv()

assistant_id = os.getenv('CHATBOT_OPENAI_ASSISTANT_ID')
server_host = os.getenv('CHATBOT_SERVER_HOST')
server_port = os.getenv('CHATBOT_SERVER_PORT')

app = Flask(__name__)

app.register_blueprint(hubspot, url_prefix='/hubspot')
app.register_blueprint(messenger, url_prefix='/messenger')
app.register_blueprint(chat, url_prefix='/chat')


assistant_id = os.getenv('CHATBOT_OPENAI_ASSISTANT_ID')


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'GET request received!'})




if __name__ == '__main__':
    app.run(host=server_host ,debug=True, port=server_port)
