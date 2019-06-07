import datetime
import decimal
import json

import botocore

# Helper class to convert AWS items to JSON.
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat()
        elif isinstance(o, botocore.response.StreamingBody):
            return o.read().decode("utf-8")
        return super(CustomJsonEncoder, self).default(o)
