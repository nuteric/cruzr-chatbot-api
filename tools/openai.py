
import json
from actions.hubspot import check_order_status, create_new_contact_if_not_found, create_ticket_in_hubspot, get_available_appointment_slots, reschedule_telemed_appointment, retrieve_telemed_appointment_details, search_hubspot_contact_by_email, verify_contact_identity
from actions.openai import add_thread_message, create_run, get_thread_last_message, retrieve_run, submit_function_outputs


def execute_action(thread_id, run_id, action):
    if not thread_id:
        return {'error': 'Thread ID is required'}
    if not run_id:
        return {'error': 'Run ID is required'}
    if not action:
        return {'error': 'action is required'}


    json_string = action['function']['arguments']
    arguments = json.loads(json_string)

    result = None

    if(action["function"]["name"] == "create_ticket_in_hubspot"):
         result = create_ticket_in_hubspot(arguments["customer_id"], arguments["customer_name"], arguments["issue_summary"])
    if(action["function"]["name"] == "retrieve_telemed_appointment_details"):
         #retrieve_telemed_appointment_details
         #result = retrieve_telemed_appointment_details(arguments["email"], arguments["first_name"], arguments["last_name"])
         result = "appointment is on Monday at 10 am"
    if(action["function"]["name"] == "search_hubspot_contact_by_email"):
         #search_hubspot_contact_by_email
         result = search_hubspot_contact_by_email(arguments["email_address"])
    if(action["function"]["name"] == "verify_contact_identity"):
         #verify_contact_identity
         result = verify_contact_identity(arguments["email_address"], arguments["mother_maiden_name"])
    if(action["function"]["name"] == "create_new_contact_if_not_found"):
         #create_new_contact_if_not_found
         result = create_new_contact_if_not_found(arguments["email_address"], arguments["first_name"], arguments["last_name"])
    if(action["function"]["name"] == "reschedule_telemed_appointment"):
         #reschedule_telemed_appointment
         #result = reschedule_telemed_appointment(arguments["email"], arguments["first_name"], arguments["last_name"], arguments["date"], arguments["time"], arguments["service"], arguments["practitioner"], arguments["location"], arguments["phone"])
         result = "appointment is rescheduled to Tuesday at 11 am"
    if(action["function"]["name"] == "get_available_appointment_slots"):
         #get_available_appointment_slots
         #result = get_available_appointment_slots()
         result = "Monday at 10 am, Tuesday at 11 am"
    if(action["function"]["name"] == "check_order_status"):
         #check_order_status
         #result = check_order_status(arguments["order_id"])
         result = "order is shipped"

    output = {
            'tool_call_id': action["id"],
            'output': result
         }

    return  output


def create_run_and_get_last_message(thread_id,assistant_id):

    create_run_response = create_run(thread_id,assistant_id)
    create_run_response_json = create_run_response.json


    run_id = create_run_response_json['id']

    retrieve_run_response = retrieve_run(thread_id,run_id)
    retrieve_run_response_json = retrieve_run_response.json

    while retrieve_run_response_json['status'] != 'completed':
        if retrieve_run_response_json['status'] == 'requires_action':
            required_action = retrieve_run_response_json['required_action']
            tool_calls = required_action['submit_tool_outputs']['tool_calls']
            tool_call_outputs = []
            for tool_call in tool_calls:
                tool_call_output = execute_action(thread_id,run_id,tool_call)
                print("tool_call_output: ", tool_call_output)
                tool_call_outputs.append(tool_call_output)
            submit_function_outputs(thread_id,run_id,tool_call_outputs)

        retrieve_run_response = retrieve_run(thread_id,run_id)
        retrieve_run_response_json = retrieve_run_response.json
        print(retrieve_run_response_json['status'])


    last_message = get_thread_last_message(thread_id)
    return last_message