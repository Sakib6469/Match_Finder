from flask import Flask

app = Flask(__name__)
# app = Flask(__name__, static_folder="static")


app.secret_key = "CleanCoder"