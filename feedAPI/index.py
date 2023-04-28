import os
from datetime import datetime
from flask import Flask, jsonify, request

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from feedAPI.model.tables import Base
from feedAPI.model.tables import Feedback
from feedAPI.model.tables import Comment

app = Flask(__name__)

# Some parameters, should end up in a file at some point
DATABASE = os.path.abspath("./database.db")
DEBUG = True

engine = create_engine("sqlite:///"+DATABASE, echo=DEBUG)

# Ugly test to create db if we start from scratch
if not os.path.isfile(DATABASE):
    Base.metadata.create_all(engine)


@app.route("/feedback")
def get_feedbacks():
    session = Session(engine)
    feedbacks = []
    for f in session.query(Feedback).all():
        feedbacks.append(f.as_dict())
    return jsonify(feedbacks)


@app.route("/feedback", methods=['POST'])
def post_feedback():
    with Session(engine) as session:
        feedback = Feedback(
            source="0.0.0.0",
            text="Awesome backend",
            grade=5,
            datetime=datetime.now()
            )
    session.add(feedback)
    print("Adding "+feedback.__str__()+" to the DB")
    session.commit()
#    feedback = request.get_data(True,True,False)
#    f = open(FEEDBACK_FILE, 'a')
#    f.write(feedback)
    return "", 204
