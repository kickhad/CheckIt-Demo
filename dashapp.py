import os

from config import Config

DEBUG = False
try:
    if os.environ['DEBUG']:
        DEBUG = True
except:
    pass

config = Config()
from app1 import create_app

server = create_app()
if __name__ == "__main__":
    server.run(host='0.0.0.0', port=5000, debug=DEBUG)
