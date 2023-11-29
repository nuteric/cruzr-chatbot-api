
import json
from actions.hubspot import check_order_status, create_new_contact_if_not_found, get_available_appointment_slots, reschedule_telemed_appointment, retrieve_telemed_appointment_details, search_hubspot_contact_by_email, verify_contact_identity
from actions.openai import add_thread_message, create_run, get_thread_last_message, retrieve_run


def execute_action(thread_id, run_id, action):
    if not thread_id:
        return {'error': 'Thread ID is required'}
    if not run_id:
        return {'error': 'Run ID is required'}
    if not action:
        return {'error': 'action is required'}


    json_string = action.function.arguments
    arguments = json.loads(json_string)

    result = None

    if(action.function.name == "handoff_to_human_agent"):
         #handoff_to_human_agent
         result = ""
    if(action.function.name == "retrieve_telemed_appointment_details"):
         #retrieve_telemed_appointment_details
         result = retrieve_telemed_appointment_details(arguments.email, arguments.firstname, arguments.lastname)
    if(action.function.name == "search_hubspot_contact_by_email"):
         #search_hubspot_contact_by_email
         result = search_hubspot_contact_by_email(arguments.email)
    if(action.function.name == "verify_contact_identity"):
         #verify_contact_identity
         result = verify_contact_identity(arguments.email, arguments.firstname, arguments.lastname)
    if(action.function.name == "create_new_contact_if_not_found"):
         #create_new_contact_if_not_found
         result = create_new_contact_if_not_found(arguments.email, arguments.firstname, arguments.lastname)
    if(action.function.name == "reschedule_telemed_appointment"):
         #reschedule_telemed_appointment
         result = reschedule_telemed_appointment(arguments.email, arguments.firstname, arguments.lastname, arguments.date, arguments.time, arguments.service, arguments.practitioner, arguments.location, arguments.phone)
    if(action.function.name == "get_available_appointment_slots"):
         #get_available_appointment_slots
         result = get_available_appointment_slots()
    if(action.function.name == "check_order_status"):
         #check_order_status
         result = check_order_status(arguments.order_id)




    return {
            'thread_id': thread_id,
            'run_id': run_id,
            'tool_call_id': action.id,
            'output': result
         }


def create_run_and_get_last_message(thread_id,assistant_id):

    create_run_response = create_run(thread_id,assistant_id)
    create_run_response_json = create_run_response.json


    run_id = create_run_response_json['id']

    retrieve_run_response = retrieve_run(thread_id,run_id)
    retrieve_run_response_json = retrieve_run_response.json

    while retrieve_run_response_json['status'] != 'completed':
        retrieve_run_response = retrieve_run(thread_id,run_id)
        retrieve_run_response_json = retrieve_run_response.json


    last_message = get_thread_last_message(thread_id)
    return last_message