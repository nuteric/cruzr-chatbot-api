import os
from flask import jsonify
import requests

access_token = None
refresh_token = None

def set_tokens(access, refresh):
    global access_token, refresh_token
    access_token = access
    refresh_token = refresh

def get_access_token():
    global access_token
    return access_token

def get_refresh_token():
    global refresh_token
    return refresh_token

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

def create_new_contact_if_not_found(email, first_name, last_name):
    if not email:
        return 'email is required'

    if not first_name:
        return 'first name is required'

    if not last_name:
        return 'last name is required'

    data = {
        'properties': {
            'email': email,
            'firstname': first_name,
            'lastname': last_name
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
    print("output: ", output)
    output_string = output['properties']['firstname'] +" "+ output['properties']['lastname']

    return output_string

def reschedule_telemed_appointment():
    return jsonify()

def get_available_appointment_slots():
    return jsonify()

def check_order_status():
    return jsonify()

def retrieve_telemed_appointment_details():
    return jsonify()