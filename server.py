
from flask import Flask, request, redirect
from flask import jsonify
from dotenv import load_dotenv




from api.hubspot import hubspot
from api.messenger import messenger
from api.openai import openai

load_dotenv()

app = Flask(__name__)

app.register_blueprint(hubspot, url_prefix='/hubspot')
app.register_blueprint(openai, url_prefix='/openai')
app.register_blueprint(messenger, url_prefix='/messenger')



@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'GET request received!'})




if __name__ == '__main__':
    app.run(host='localhost' ,debug=True, port=5001)
