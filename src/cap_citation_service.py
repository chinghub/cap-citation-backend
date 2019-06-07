import json
import logging
import os
import time

from functools import wraps

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from dotenv import load_dotenv

from controllers import case_controller
#from util.logging_util import initialize_logging
from util.json_dumper import CustomJsonEncoder

# APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
APP_ROOT = os.getcwd()
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)

LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
)
# don't allow boto to log at DEBUG level - it is way too chatty
logging.getLogger("botocore").setLevel(logging.WARN)
logging.getLogger("boto3").setLevel(logging.WARN)
logging.getLogger("urllib3").setLevel(logging.WARN)

# initialize_logging()

# ---- app setup -----------------------

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["15 per minute", "100 per hour"]
)

# ----- middleware ----------------------


@app.before_request
def before_request():
    LOGGER.debug({"message": "before request", "request": request.get_data()})


@app.after_request
def after_request(response):
    LOGGER.debug(
        {
            "message": "after request",
            "resp": response.get_data(),
            "headers": response.headers,
            "status code": response.status_code,
        }
    )
    return response


def route_wrapper(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            return f(*args, **kwargs)
        except Exception:
            LOGGER.exception("unexpected error")
            return jsonify({"status": "ERROR"})  # TODO
        finally:
            elapsed_time = time.perf_counter() - start_time
            LOGGER.info(
                {
                    "message": "execution finished",
                    "function": f.__name__,
                    "duration": elapsed_time,
                }
            )
            # TODO - write metric to CloudWatch

    return decorated_function


# ----- routes -------------------------


@app.route("/case", methods=(["POST"]))
@route_wrapper
def get_case():
    return Response(
        json.dumps(case_controller.get_case(request.json), cls=CustomJsonEncoder),
        mimetype="application/json",
    )


@app.route("/")
def index():
    return jsonify({"message": "cap-citation", "version": "0.1"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1776)
