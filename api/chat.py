from flask import Blueprint, request, jsonify
import os
from actions.openai import add_thread_message, get_thread_messages
from tools.openai import create_run_and_get_last_message

assistant_id = os.getenv('VITALITY_RX_OPENAI_ASSISTANT_ID')
chat = Blueprint('chat', __name__)

@chat.route('/', methods=['GET'])
def get_chat():
    # Your code here to handle a GET request
    thread_id = request.args.get('thread_id')
    message = get_thread_messages(thread_id)
    return message

@chat.route('/', methods=['POST'])
def post_chat():

    thread_id = request.json.get('thread_id')
    message = request.json.get('message')

    add_thread_message(thread_id,message)

    last_message = create_run_and_get_last_message(thread_id,assistant_id)

    return last_message