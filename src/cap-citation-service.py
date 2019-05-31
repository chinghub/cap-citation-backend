import json
import logging
import time

from functools import wraps

from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from controllers import refs_controller

# from dotenv import load_dotenv, find_dotenv
#
# dotenv = Dotenv(os.path.join(os.path.dirname(__file__), ".env"))
# os.environ.update(dotenv)
# CAP_TOKEN = os.environ.get("CAP_TOKEN") # TODO

LOGGER = logging.getLogger(__name__)

# ---- app setup -----------------------

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[
        "15 per minute",
        "100 per hour"
    ]
)

# ----- middleware ----------------------


@app.before_request
def before_request():
    LOGGER.debug({'message': 'before request', 'request': request.get_data()})

@app.after_request
def after_request(response):
    LOGGER.debug({ 'message': 'resp', 'resp': response.get_data(), 'headers': response.headers, 'status code': response.status_code, })
    return response


def route_wrapper(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            return f(*args, **kwargs)
        except Exception:
            LOGGER.exception('unexpected error')
            return jsonify({}) # TODO
        finally:
            elapsed_time = time.perf_counter() - start_time
            LOGGER.info({
                'message': 'execution finished',
                'function': f.__name__,
                'duration': elapsed_time
            })
            # TODO - write metric to CloudWatch
    return decorated_function



# ----- routes -------------------------

@app.route('/get-refs', methods=['POST'])
@route_wrapper
def get_refs():
    return refs_controller.get_refs(request.json)

@app.route('/')
def index():
    return jsonify({"message": "cap-citation", "version": "0.1"})

if __name__ == '__main__':
 app.run()
