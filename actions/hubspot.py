import os
from flask import jsonify
import requests

access_token = os.getenv('VITALITY_RX_HUBSPOT_ACCESS_TOKEN')

def search_hubspot_contact_by_email(email):

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/contacts/search',
        json={'query': email},
        headers={
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
    )

    if response.status_code != 200:
        return jsonify({'error': 'Error searching contact'}), 500

    return jsonify(response.json())

def verify_contact_identity(email, firstname, lastname):

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    if not firstname:
        return jsonify({'error': 'Firstname is required'}), 400

    if not lastname:
        return jsonify({'error': 'Lastname is required'}), 400


    return jsonify()

def create_new_contact_if_not_found(email, firstname, lastname):
    if not email:
        return jsonify({'error': 'email is required'}), 400

    if not firstname:
        return jsonify({'error': 'firstname is required'}), 400

    if not lastname:
        return jsonify({'error': 'lastname is required'}), 400

    data = {
        'properties': {
            'email': email,
            'firstname': firstname,
            'lastname': lastname
        }
    }


    response = requests.post('https://api.hubapi.com/crm/v3/objects/contacts',
        headers={
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        },
        json=data
    )

    if response.status_code != 201:
        return jsonify({'error': 'Error adding contact'}), 500

    return jsonify(response.json())

def reschedule_telemed_appointment():
    return jsonify()

def get_available_appointment_slots():
    return jsonify()

def check_order_status():
    return jsonify()

def retrieve_telemed_appointment_details():
    return jsonify()