import os
from pathlib import Path
from dotenv import load_dotenv

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(Path(basedir) / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32))

# Enable debug mode.
DEBUG = True

# Connect to the database


SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URI:
    raise RuntimeError(
        "DATABASE_URL is not set. Add it to a .env file or export it in your shell."
    )

SQLALCHEMY_TRACK_MODIFICATIONS = False
