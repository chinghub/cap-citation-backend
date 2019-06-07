from link_extraction import regex_extractor_1

CONFIDENCE_LOW="LOW"

class Link:

    def __init__(self, url, method, confidence):
        self.url = url
        self.method = method
        self.confidence = confidence

    def to_dict(self):
        return {
            'url': self.url,
            'method': self.method,
            'confidence': self.confidence
        }

def extract_urls_from_text(text):
    """
    given a text string, extract any urls and return them with a confidence score

    example return body:

    [
        {
            "url": "...",
            "confidence": "HIGH"
        }
    ]
    """

    return [
        Link(url=url, method='re1', confidence=CONFIDENCE_LOW)
        for url
        in regex_extractor_1.process_text(text)
    ]
