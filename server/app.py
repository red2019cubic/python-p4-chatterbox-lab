from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/messages')
def fetch_all_messages():
    messages = Message.query.all()
    messages_list = [message.to_dict() for message in messages]
    response = make_response(messages_list, 200)
    return response


@app.route('/messages', methods=['POST',])
def create_message():
    msg = request.get_json()
    new_message = Message(body=msg["body"], username=msg["username"])
    db.session.add(new_message)
    db.session.commit()
    return new_message.to_dict()


@app.route('/messages/<int:id>')
def messages_by_id(id):
    message = Message.query.get(id)
    response = make_response(message.to_dict(), 200)
    return response


@app.route('/messages/<int:id>', methods=['PATCH',])
def update_message(id):
    message = Message.query.get(id)
    msg = request.get_json()
    message.body = msg["body"]
    db.session.add(message)
    db.session.commit()
    response = make_response(message.to_dict(), 200)
    return response


@app.route('/messages/<int:id>', methods=['DELETE',])
def delete_message(id):
    message = Message.query.get(id)
    db.session.delete(message)
    db.session.commit()
    return "Record Deleted"


if __name__ == '__main__':
    app.run(port=5555)
