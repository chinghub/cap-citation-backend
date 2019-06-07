from datetime import datetime

import requests

from link_extraction import link_extractor

CONFIDENCE_MED="MED"
CONFIDENCE_LOW="LOW"

class Ref:

    def __init__(self, url, retrieved_status_code, retrieved_body, retrieval_time, confidence):
        self.url = url
        self.retrieved_status_code = retrieved_status_code
        self.retrieved_body = retrieved_body
        self.retrieval_time = retrieval_time
        self.confidence = confidence

    def to_dict(self):
        return {
        'url': self.url,
        'retrieved_status_code': self.retrieved_status_code,
        'retrieved_body': self.retrieved_body,
        'retrieval_time': self.retrieval_time,
        'confidence': self.confidence

        }


    @classmethod
    def retrieve_url(cls,url):
        # defaults
        retrieved_status_code="-1"
        retrieved_body=""
        retrieval_time=int(datetime.utcnow().timestamp())
        confidence=CONFIDENCE_LOW

        try:
            resp = requests.get(url)

            retrieved_status_code=resp.status_code
            retrieved_body=resp.json()
            retrieval_time=int(datetime.utcnow().timestamp())
            if retrieved_status_code == 200:
                confidence=CONFIDENCE_MED

        except:

            try:
                # https://archive.org/help/wayback_api.php
                wayback_url = f"http://archive.org/wayback/available?url={url}"
                wayback_resp = requests.get(wayback_url)
                if 'archived_snapshots' in wayback_resp.json():
                    snapshots = resp.get('archived_snapshots')
                    if 'closest' in snapshots:
                       r = requests.get(snapshots.get('closest').get('url'))

                    retrieved_status_code=r.status_code
                    retrieved_body=r.json()
                    retrieval_time=int(datetime.utcnow().timestamp())
                    confidence=CONFIDENCE_LOW

            except:
                pass

        return [Ref(url, retrieved_status_code, retrieved_body, retrieval_time, confidence)]

class LinkRef:

    def __init__(self, link, refs=[]):
        self.link = link
        self.refs=refs

    def add_ref(self, ref):
        self.refs.append(ref)

    def to_dict(self):
        return {
            'link': self.link.to_dict(),
            'refs': [ ref.to_dict() for ref in self.refs ]
        }

def process_case(case_body):
    linkrefs = []
    for opinion in case_body['data'].get('opinions', []):
        for link in link_extractor.extract_urls_from_text(opinion['text']):

            refs = Ref.retrieve_url(link.url)
            linkrefs.append(LinkRef(link, refs))

    return linkrefs
