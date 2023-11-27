from flask import Blueprint, request, jsonify
import os
import requests

openai = Blueprint('openai', __name__)

thread_id = None

api_key = os.getenv('VITALITY_RX_OPENAI_API_KEY')

def set_thread_id(id):
    global thread_id
    thread_id = id

def get_thread_id():
    global thread_id
    return thread_id


@openai.route('/create-thread', methods=['POST'])
def create_thread():

    print("api_key: " + api_key)


    response = requests.post(
        'https://api.openai.com/v1/threads',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'}
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    print(response.json()['id'])
    set_thread_id(response.json()['id'])

    return jsonify(response.json())

@openai.route('/add-thread-message', methods=['POST'])
def add_thread_message():

    print("api_key: " + api_key)

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

@openai.route('/get-thread-messages', methods=['GET'])
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

@openai.route('/create-run', methods=['POST'])
def create_run():

    print("api_key: " + api_key)
    print(request.json)

    thread_id = request.json.get('thread_id')
    assistant_id = request.json.get('assistant_id')
    # assistant_id = "asst_vIB1qC7Macce1ujVxKbkwqhq"
    instructions = request.json.get('instructions')

    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400
    if not assistant_id:
        return jsonify({'error': 'Assistant ID is required'}), 400

    response = requests.post(
        'https://api.openai.com/v1/threads/'+ thread_id +'/runs',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
        json={'assistant_id': assistant_id, 'instructions':instructions}
    )

    if response.status_code != 200:
        print(response.json())
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

@openai.route('/retrieve-run', methods=['GET'])
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

@openai.route('/submit-function-outputs', methods=['POST'])
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
