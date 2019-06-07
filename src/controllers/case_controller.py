import json
import logging

from cap_client import cap

from db.citation_ref_db import CapCase, CapCaseRef
from processor import case_processor

LOGGER = logging.getLogger(__name__)

def get_case(request_dict):
    cap_case_id = request_dict.setdefault("payload", {}).get("capId")
    return get_case_by_id(cap_case_id)


def get_case_by_id(cap_case_id):
    # TODO - look up existing refs
    #        if none exist, get case body, extract text, do lookup, write to db, and return

    # eventually return token to caller for async ops

    case = CapCase.get_by_id(cap_case_id)
    if case:
        case = case['Document']
    else:
        cap_resp = cap.get_case(cap_case_id)

        if cap_resp.get('count', 0) > 0:
            CapCase.save(cap_case_id, cap_resp['results'][0])
        else:
            raise Exception("unable to retrieve case")

    refs = CapCaseRef.get_latest_ref_by_id(cap_case_id)
    if not refs:
        refs = case_processor.process_case(case['casebody'])
        refs = json.dumps([ ref.to_dict() for ref in refs ])
        CapCaseRef.save(cap_case_id, document=refs)

    return {"status": "SUCCESSFUL", "payload": {"case_id": cap_case_id, "case": case, 'refs': refs}}
