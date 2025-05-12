import os

STORE_HOST = os.environ.get("STORE_HOST") or "localhost"
STORE_PORT = os.environ.get("STORE_PORT") or 8000


USER_ID = os.environ.get("USER_ID") or 1