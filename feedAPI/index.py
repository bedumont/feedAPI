from flask import Flask, jsonify, request

app = Flask(__name__)

comment = [
        {'ip': '0:0:0:0',
         'text': 'This is a comment',
         'rating': 3
         }
]


@app.route("/feedback")
def hello_world():
    return "Hello, World !"
