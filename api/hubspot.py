from flask import Blueprint, request, jsonify
import os
import requests

hubspot = Blueprint('hubspot', __name__)

access_token = os.getenv('VITALITY_RX_HUBSPOT_ACCESS_TOKEN')
refresh_token = os.getenv('VITALITY_RX_HUBSPOT_REFRESH_TOKEN')

@hubspot.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    code = request.args.get('code')

    if not code:
        return jsonify({'error': 'Authorization code is required'}), 400

    client_id = os.getenv('VITALITY_RX_HUBSPOT_CLIENT_ID')
    client_secret = os.getenv('VITALITY_RX_HUBSPOT_CLIENT_SECRET')
    redirect_uri = os.getenv('VITALITY_RX_HUBSPOT_REDIRECT_URI')

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

@hubspot.route('/send-booking-email-confirmation',methods=['POST'])
def send_booking_email_confirmation():
    email = request.json.get('email')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    date = request.json.get('date')
    time = request.json.get('time')
    service = request.json.get('service')
    practitioner = request.json.get('practitioner')
    location = request.json.get('location')
    phone = request.json.get('phone')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    if not first_name:
        return jsonify({'error': 'First name is required'}), 400

    if not last_name:
        return jsonify({'error': 'Last name is required'}), 400

    # response = requests.post(
    #     'https://api.hubapi.com/emails/v1/singleEmail/send',
    #     params={'hapikey': access_token},
    #     json={
    #         "emailId": 1111111111,
    #         "message": {
    #             "to": email,
    #             "from": "",
    #             "cc": "",
    #             "bcc": "",
    #             "subject": "Your Booking Confirmation",
    #             "text": "This is a confirmation of your booking.",
    #             "html": "<html><body><p>Hi "+first_name+",</p><p>This is a confirmation of your booking.</p><p><strong>Booking Details</strong></p><p><strong>Date:</strong> "+date+"</p><p><strong>Time:</strong> "+time+"</p><p><strong>Service:</strong> "+service+"</p><p><strong>Practitioner:</strong> "+practitioner+"</p><p><strong>Location:</strong> "+location+"</p><p><strong>Phone:</strong> "+phone+"</p><p><strong>Thank you!</strong></p></body></html>"
    #         }
    #     }
    # )

    # if response.status_code != 200:
    #     return jsonify({'error': 'Error sending email'}), 500

    test_response = {
        "message": "Booking confirmation sent to email"
    }

    return jsonify(test_response)

@hubspot.route('/search-contact', methods=['POST'])
def search_contact():
    email = request.json.get('email')

    print(email)

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