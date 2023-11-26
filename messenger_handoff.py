from flask import jsonify

def handle_messenger_handoff(request):
    # Return a fake JSON response
    return jsonify({
        "status": "success",
        "message": "handed to a human agent",
        "agent": "Kristoffe Abellera"
    })