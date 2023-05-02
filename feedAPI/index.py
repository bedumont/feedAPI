import os
import re
from datetime import datetime
from flask import Flask, jsonify, request

from sqlalchemy.orm import Session
from sqlalchemy import func, create_engine, select, exc

from feedAPI.model.tables import Base
from feedAPI.model.tables import Feedback
from feedAPI.model.tables import Comment
from feedAPI.model.tables import Reaction

app = Flask(__name__)

# Some parameters, should end up in a file at some point
DATABASE = os.path.abspath("./database.db")
DEBUG = True

engine = create_engine("sqlite:///"+DATABASE, echo=DEBUG)

# Ugly test to create db if we start from scratch
if not os.path.isfile(DATABASE):
    Base.metadata.create_all(engine)


@app.route("/feedback", methods=['GET'])
def get_all_feedbacks():
    """ Retrieves all feedbacks
    Uses a GET call to route /feedback
    Returns a json and code 200 in case of success
    """
    session = Session(engine)
    feedbacks = []
    for f in session.query(Feedback).all():
        feedbacks.append(f.as_dict())
    return jsonify(feedbacks), 200


@app.route("/feedback/<id>/comments", methods=['GET'])
def get_feedback_comments(id):
    """ Retrieves comments to feedback <id>
    Uses a GET call to route /feedback/<id>/comments
    Returns a json and code 200 in case of success
    """
    session = Session(engine)
    stmt = select(Comment).where(Comment.target.is_(id))
    comments = []
    for f in session.scalars(stmt):
        comments.append(f.as_dict())
    return ('', 404) if len(comments) == 0 else (jsonify(comments), 200)


@app.route("/feedback/<id>", methods=['GET'])
@app.route("/comment/<id>", methods=['GET'])
def get_resource(id):
    """ Retrieves a resource with id <id> (Feedback or Comment)
    Uses a GET call to route /[typeOfResource]/<id>
    Returns a json with the requested resource and code 200 in case of success
    """
    typeOfResource = Feedback if re.search("^/feedback", request.path) else Comment
    session = Session(engine)
    stmt = select(Feedback).where(Feedback.id.is_(id))
    try:
        resource = session.scalars(stmt).one()
        return (jsonify(resource.as_dict()), 200)
    except exc.NoResultFound:
        return 'Resource was not found', 404
    except exc.MultipleResultsFound:
        return 'Internal error: multiple resources with same id', 500


@app.route("/feedback", methods=['POST'])
@app.route("/comment", methods=['POST'])
def create_resource():
    """ Creates a resource (Feedback or Comment)
    Uses a POST call to route /[typeOfResource]
    Expects resource data as json
    Returns code 201 on success
    """
    typeOfResource = Feedback if re.search("^/feedback", request.path) else Comment
    data = request.get_json()
    timestamp = int(data["datetime"])
    data["datetime"] = datetime.fromtimestamp(timestamp)
    with Session(engine) as session:
        resource = typeOfResource(data)
        session.add(resource)
        print("Adding "+resource.__str__()+" to the DB")
        session.commit()
    return "Resource added", 201


@app.route("/feedback/<id>", methods=['PUT'])
@app.route("/comment/<id>", methods=['PUT'])
def react_to_comment(id):
    """ Reacts to comment <id>
    Uses a PUT call to route /[typeOfResource]/<id> (typeOfResource can be Feedback or Comment
    Ignores cmt_id and fb_id and replaces each with <id> or None based on the path
    Returns code 201 in case of success
    """
    if re.search("^/feedback", request.path):
        resourceType = Feedback
        fb_id = id
        cmt_id = None
    else:
        resourceType = Comment
        fb_id = None
        cmt_id = id
    data = request.get_json()
    data["fb_id"] = fb_id
    data["cmt_id"] = cmt_id
    if data["value"] not in ["-1", "1"]:
        return "Bad value provided", 400
    stmt = select(resourceType).where(resourceType.id.is_(id))
    timestamp = int(data["datetime"])
    data["datetime"] = datetime.fromtimestamp(timestamp)
    with Session(engine) as session:
        try:
            resource = session.scalars(stmt).one()
            reaction = Reaction(data)
            session.add(reaction)
            print("Adding "+reaction.__str__()+" to the DB")
            resource.score += int(data["value"])
            print("Updating score of "+resource.__str__())
            return "Reaction added", 201
        except exc.NoResultFound:
            return 'Parent resource was not found', 404
        except exc.MultipleResultsFound:
            return 'Internal error: multiple resources with same id', 500
        finally:
            session.commit()


@app.route("/reaction", methods=['GET'])
def get_all_reactions():
    """ Retrieves all feedbacks
    Uses a GET call to route /feedback
    Returns a json and code 200 in case of success
    """
    session = Session(engine)
    reactions = []
    for r in session.query(Reaction).all():
        reactions.append(r.as_dict())
    return jsonify(reactions), 200


@app.route("/test", methods=["GET"])
def sum_values():
    session = Session(engine)
    Feedback.check_score(session)
#    query = session.query(
#        Feedback.id,
#        Feedback.score,
#        func.sum(Reaction.value)
#    ).join(Reaction.feedback
#    ).group_by(Reaction.fb_id)
#    for r in query.all():
#        print(r)
    return '', 200
