from flask import Blueprint, request, jsonify
import os
import requests
from messenger_handoff import handle_messenger_handoff


messenger = Blueprint('messenger', __name__)


@messenger.route('/handoff', methods=['POST'])
def messenger_handoff():
    return handle_messenger_handoff(request)

@messenger.route('/callback', methods=['GET','POST'])
def messenger_callback():
    if request.method == 'POST':
        # Handle the message
        print(request.json)
        return 'Message received'
    elif request.method == 'GET':
        if(request.args.get('hub.verify_token') == 'vitality-rx'):
            return request.args.get('hub.challenge')