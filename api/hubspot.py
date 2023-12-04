from flask import Blueprint, request, jsonify
import os
import requests

hubspot = Blueprint('hubspot', __name__)

access_token = os.getenv('CHATBOT_HUBSPOT_ACCESS_TOKEN')
refresh_token = os.getenv('CHATBOT_HUBSPOT_REFRESH_TOKEN')

@hubspot.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    code = request.args.get('code')

    if not code:
        return jsonify({'error': 'Authorization code is required'}), 400

    client_id = os.getenv('CHATBOT_HUBSPOT_CLIENT_ID')
    client_secret = os.getenv('CHATBOT_HUBSPOT_CLIENT_SECRET')
    redirect_uri = os.getenv('CHATBOT_HUBSPOT_REDIRECT_URI')

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

    return jsonify({'access_token': access_token, 'refresh_token': refresh_token})

