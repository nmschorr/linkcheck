
import os
PORT = '5000'

PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 5000))
GUNICORN_CMD_ARGS="--bind=0.0.0.0"

