from flask import Blueprint, request, jsonify
import os
import requests
import json

from actions.hubspot import search_hubspot_contact_by_email, verify_contact_identity, create_new_contact_if_not_found, reschedule_telemed_appointment, get_available_appointment_slots, check_order_status, retrieve_telemed_appointment_details

openai = Blueprint('openai', __name__)

api_key = os.getenv('VITALITY_RX_OPENAI_API_KEY')




def create_thread():
    response = requests.post(
        'https://api.openai.com/v1/threads',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'}
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

def add_thread_message(thread_id, message):

    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    response = requests.post(
        'https://api.openai.com/v1/threads/'+ thread_id +'/messages',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
        json={'role': 'user','content':message}
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

def get_thread_messages(thread_id):

    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400

    response = requests.get(
        'https://api.openai.com/v1/threads/'+ thread_id +'/messages',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

def get_thread_last_message(thread_id):

    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400

    response = requests.get(
        'https://api.openai.com/v1/threads/'+ thread_id +'/messages',
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500


    last_message = response.json()['data'][0]

    return jsonify(last_message)

def create_run(thread_id, assistant_id, instructions=None):

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
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

def retrieve_run(thread_id, run_id):

    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400
    if not run_id:
        return jsonify({'error': 'Run ID is required'}), 400

    response = requests.get(
        'https://api.openai.com/v1/threads/'+ thread_id +'/runs/'+ run_id,
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

def submit_function_outputs(thread_id, run_id, tool_outputs):
    if not thread_id:
        return jsonify({'error': 'Thread ID is required'}), 400
    if not run_id:
        return jsonify({'error': 'Run ID is required'}), 400
    if not tool_outputs:
        return jsonify({'error': 'Tool outputs is required'}), 400

    response = requests.post(
        'https://api.openai.com/v1/threads/'+ thread_id +'/runs/'+ run_id +"/submit_tool_outputs",
        headers={'Authorization': 'Bearer ' + api_key, 'Content-Type': 'application/json', 'OpenAI-Beta':'assistants=v1'},
        json={'tool_outputs': tool_outputs}
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error interacting with OpenAI API'}), 500

    return jsonify(response.json())

