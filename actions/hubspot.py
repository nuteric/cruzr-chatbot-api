import os
from flask import jsonify
import requests

access_token = os.getenv('CHATBOT_HUBSPOT_ACCESS_TOKEN')

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
        return 'Error searching contact'

    output = response.json()

    if output['total'] == 0:
        return 'Contact not found'
    output_string = output['results'][0]['properties']['firstname'] +" "+ output['results'][0]['properties']['lastname']

    return output_string

def verify_contact_identity(email, verification_code):

    if not email:
        return 'Email is required'

    if not verification_code:
        return 'Verification code is required'



    return "verified"

def create_new_contact_if_not_found(email, firstname, lastname):
    if not email:
        return 'email is required'

    if not firstname:
        return 'firstname is required'

    if not lastname:
        return 'lastname is required'

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

    output = response.json()
    print(output)
    output_string = output['results'][0]['properties']['firstname'] +" "+ output['results'][0]['properties']['lastname']

    return output_string

def reschedule_telemed_appointment():
    return jsonify()

def get_available_appointment_slots():
    return jsonify()

def check_order_status():
    return jsonify()

def retrieve_telemed_appointment_details():
    return jsonify()