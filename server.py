import os
from dotenv import load_dotenv
import requests
from flask import Flask, request, redirect
from flask import jsonify

from messenger_handoff import handle_messenger_handoff

load_dotenv()


app = Flask(__name__)

api_key = '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'

thread_id = None

def set_thread_id(id):
    global thread_id
    thread_id = id

def get_thread_id():
    global thread_id
    return thread_id

@app.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    code = request.args.get('code')

    if not code:
        return jsonify({'error': 'Authorization code is required'}), 400

    client_id = os.getenv('HUBSPOT_CLIENT_ID')
    client_secret = os.getenv('HUBSPOT_CLIENT_SECRET')
    redirect_uri = os.getenv('HUBSPOT_REDIRECT_URI')

    response = requests.post(
        'https://api.hubapi.com/oauth/v1/token',
        data={
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'code': code
        }
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error getting access token'}), 500

    access_token = response.json().get('access_token')
    refresh_token = response.json().get('refresh_token')

    # Your code here

    return jsonify({'access_token': access_token, 'refresh_token': refresh_token})

@app.route('/test', methods=['GET'])
def test():
    return 'GET request received!'

@app.route('/create-thread', methods=['POST'])
def create_thread():

    response = requests.post(
        'https://api.openai.com/v1/threads',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'}
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    set_thread_id(response.json()['id'])

    return jsonify(response.json())

@app.route('/add-thread-message', methods=['POST'])
def add_thread_message():

    thread_id = request.json.get('thread_id')
    message = request.json.get('message')

    print(thread_id)

    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400

    response = requests.post(
        'https://api.openai.com/v1/threads/'+ thread_id +'/messages',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
        json={'role': 'user','content':message}
    )

    if response.status_code != 200:
        print(response.json())
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

@app.route('/get-thread-messages', methods=['GET'])
def get_thread_messages():

    thread_id = request.args.get('thread_id')

    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400

    response = requests.get(
        'https://api.openai.com/v1/threads/'+ thread_id +'/messages',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
    )

    if response.status_code != 200:
        print(response.json())
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

@app.route('/create-run', methods=['POST'])
def create_run():

    thread_id = request.json.get('thread_id')
    assistant_id = request.json.get('assistant_id')

    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400

    response = requests.post(
        'https://api.openai.com/v1/threads/'+ thread_id +'/runs',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
        json={'assistant_id': assistant_id}
    )

    if response.status_code != 200:
        print(response.json())
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

@app.route('/retrieve-run', methods=['GET'])
def retrieve_run():

    thread_id = request.args.get('thread_id')
    run_id = request.args.get('run_id')

    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400
    if not run_id:
        return jsonify({'error': 'Run ID is required'}), 400

    response = requests.get(
        'https://api.openai.com/v1/threads/'+ thread_id +'/runs/'+ run_id,
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
    )

    if response.status_code != 200:
        print(response.json())
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    print(response.json().get('required_action'))


    return jsonify(response.json())

@app.route('/submit-function-outputs', methods=['POST'])
def submit_function_outputs():

    thread_id = request.json.get('thread_id')
    run_id = request.json.get('run_id')
    tool_call_id = request.json.get('tool_call_id')
    output = request.json.get('output')

    tool_outputs = [
        {
            "tool_call_id": tool_call_id,
            "output": output
        }
    ]

    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400
    if not run_id:
        return jsonify({'error': 'Run ID is required'}), 400
    if not tool_call_id:
        return jsonify({'error': 'Tool Call ID is required'}), 400
    if not output:
        return jsonify({'error': 'Output is required'}), 400

    response = requests.post(
        'https://api.openai.com/v1/threads/'+ thread_id +'/runs/'+ run_id +"/submit_tool_outputs",
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
        json={'tool_outputs': tool_outputs}
    )

    if response.status_code != 200:
        print(response.json())
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

@app.route('/messenger-handoff', methods=['POST'])
def messenger_handoff():
    return handle_messenger_handoff(request)

@app.route('/messenger-callback', methods=['GET','POST'])
def messenger_callback():
    if request.method == 'POST':
        # Handle the message
        print(request.json)
        return 'Message received'
    elif request.method == 'GET':
        if(request.args.get('hub.verify_token') == 'vitality-rx'):
            return request.args.get('hub.challenge')


if __name__ == '__main__':
    app.run(host='localhost' ,debug=True, port=5001)
