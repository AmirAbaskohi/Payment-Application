import json
from flask import Flask, request
import database
from utils import verify_password

# Creating an instance of our database service
DB = database.DatabaseDriver()

# Creating flask app
app = Flask(__name__)

# Function to return success response
def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code

# Function to return failure response
def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code

# This api will return all the users in the system
@app.route("/")
@app.route("/api/users/")
def get_all_users():
    return success_response(DB.get_all_users())

# This api will get the parameters from request body and creates a new user
@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    name = body["name"]
    username = body["username"]
    balance = int(body.get("balance", 0))
    password = body.get("password", "")
    email = body.get("email", "")
    user_id = DB.insert_user_table(name,username,balance,password,email)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("Something went wrong while creating user!")
    return success_response(user, 201)

# This api will return an specific user by giving id to it
@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("User not found!")
    return success_response(user)

# This api will update user inforrmation
@app.route("/api/user/<int:user_id>/", methods=["POST"])
def update_user(user_id):
    body = json.loads(request.data)
    name = body["name"]
    username = body["username"]
    balance = int(body.get("balance", 0))
    password = body.get("password", "")
    email = body.get("email", "")
    DB.update_user_by_id(name,username,balance,password,email)

    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("User not found!")
    return success_response(user)

# This api will delete an specific user by giving id to it
@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = DB.get_user_by_id(user_id)
    if user is None:
        return failure_response("User not found!")
    DB.delete_user_by_id(user_id)
    return success_response(user)

# This api will send money to a user
@app.route("/api/send/", methods=["POST"])
def create_send():
    body = json.loads(request.data)
    sender_id = int(body["sender_id"])
    receiver_id = int(body["receiver_id"])
    amount = int(body["amount"])
    password = body.get("password", "")

    sender_user = DB.get_user_by_id(sender_id)
    sender_name = sender_user["name"]
    sender_username = sender_user["username"]
    sender_balance = sender_user["balance"]
    sender_password = sender_user["password"]

    if not verify_password(sender_password, password): #password != sender_password:
        return failure_response("Incorrect password!")
    receiver_user = DB.get_user_by_id(receiver_id)
    receiver_name = receiver_user["name"]
    receiver_username = receiver_user["username"]
    receiver_balance = receiver_user["balance"]
    if amount > sender_balance:
        return failure_response("Not enough balance!")

    DB.update_user_by_id(sender_id, sender_name, sender_username, sender_balance-amount)
    DB.update_user_by_id(receiver_id, receiver_name, receiver_username, receiver_balance+amount)

    send = {"sender_id": sender_id, "receiver_id": receiver_id, "amount": amount}
    return success_response(send, 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)