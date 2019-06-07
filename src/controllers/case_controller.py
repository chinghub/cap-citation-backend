from cap_client import cap

def get_case(request_dict):
    cap_case_id = request_dict.setdefault('payload', {}).get('capId')
    # TODO - look up existing refs
    #        if none exist, get case body, extract text, do lookup, write to db, and return

    # eventually return token to caller for async ops

    print()
    print(request_dict)
    print()

    case = cap.get_case(cap_case_id)

    return {
        'status': "SUCCESSFUL",
        'payload': {
            'case_id': cap_case_id,
            'case': case
        }
    }
