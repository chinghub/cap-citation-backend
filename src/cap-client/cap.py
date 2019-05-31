import os
import requests
from urllib import parse

BASE_URL="https://api.case.law/v1/"

ENDPOINTS = {
    "cases": "cases/",
    "citations": "citations/",
    "jurisdictions": "jurisdictions/",
    "courts": "courts/",
    "volumes": "volumes/",
    "reporters": "reporters/",
    "bulk": "bulk/"
}

CASE_JURISTICTIONS= ["wash", "ill"]
CASE_FORMATS = ["xml", "html", "text"]
PAGINATION="page_size={}"

DATE_MIN_KEY='decision_date_min' # e.g. 1994-12-30
DATE_MAX_KEY='decision_date_max' # e.g. 2100-12-30

AUTH_HEADER = "Authorization: Token {}"

cap_token = os.getenv("CAP_TOKEN")

class Case():
    def __init__(self, id, jurisdiction, name, name_abbreviation, reporter, url, volume, citations, court, decision_date, docket_number, first_page, last_page, casebody):
        self.id = id
        self.jurisdiction = jurisdiction
        self.name = name
        self.name_abbreviation = name_abbreviation
        self.reporter = reporter
        self.url = url
        self.volume = volume
        self.citations = citations
        self.counrt = court
        self.decision_date = decision_date
        self.docket_number = docket_number
        self.first_page = first_page
        self.last_page = last_page
        self.casebody = casebody

    @classmethod
    def from_dict(cls):
        return cls()


def get_cases(jurisdiction, start_date, end_date="2020-01-01"):
    headers = {"Authorization": "Token {}".format(cap_token)}

    args = {
        "jurisdiction":jurisdiction,
        "full_case":"true",
        "body_format":"text",
        #"page_size":page_size,
        "decision_date_min":start_date,
        "decision_date_max":end_date
    }

    url = BASE_URL + ENDPOINTS['cases'] + "?" + parse.urlencode(args)

    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        raise Exception('error ({}) calling api: {}'.format(r.status_code, r.json()))

    results = []
    batch=1

    data = r.json()
    results.extend(data['results'])

    # print(data['next'])
    # print(data['previous'])
    print(data['count'])

    try:
        while 'next' in data and data['next']:
            batch += 1
            print('batch {} total: {}'.format(batch, len(results)))
            r = requests.get(url=data['next'], headers=headers)
            if r.status_code != 200:
                raise Exception()
            data = r.json()
            results.extend(data['results'])
    except:
        pass


    return results
