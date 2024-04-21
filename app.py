from os import getenv
from flask import Flask

app = Flask(__name__, static_url_path="/static", static_folder="static")
app.secret_key = getenv("SECRET_KEY")

import routes
