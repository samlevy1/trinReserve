from flask import jsonify
from flask import request
import os
import sys

fpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
sys.path.insert(0,fpath)

from models import UsersModel
# from db_server.models import ClubsModel
# from db_server.models import ClubLeadersModels
# from UsersModel import *
# from GamesModel import *
# from ScorecardsModel import *

trinReserve_db_name=f"{os.getcwd()}/models/trinReserveDB.db"


users = UsersModel.User(trinReserve_db_name)
# games = ClubsModel.Game(yahtzee_db_name)
# scorecards = ClubLeadersModels.Scorecard(yahtzee_db_name)

def c_rUsers():
    
    # curl "http://127.0.0.1:5000/users"

    if request.method == "GET":
        response = users.get_users()
        print(f"the response is {response['message']}")
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
        #     return [] 
        
    elif request.method == "POST":
        #curl -X POST -H "Content-type: application/json" -d '{"email":"help@trinityschoolnyc.org","password":"123TriniT", "administrator": "0"}' "http://127.0.0.1:5000/users"
        # return jsonify(request.json)
        response = users.create_user(request.json)
        print(f"the response is {response['message']}")
        # if response["result"] == "success":
        return jsonify(response["message"])
        # if response["result"] == "success":
        #     return jsonify(response["message"])
        # else:
        #     return {}    
    
def rUser_u_d(email_id):
    if request.method == "GET":
        #  curl "http://127.0.0.1:5000/users/help@trinityschoolnyc.org"
        response = users.get_user(email = email_id)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   

    elif request.method == "PUT":
        #curl -X PUT -H "Content-type: application/json" -d '{"id":8490684713803214,"email":"help@trinityschoolnyc.org", "password":"newPassword", "administrator": "1"}' "http://127.0.0.1:5000/users/help@trinityschoolnyc.org"

        response = users.update_user(request.json)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
        #     return {}   
 
    elif request.method == "DELETE":
        # curl -X DELETE "http://127.0.0.1:5000/users/help@trinityschoolnyc.org"
        response = users.remove_user(email_id)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
            # return {}   
def get_user_id(id):
    response = users.get_user(id = id)
    if response["result"] == "success":
        return jsonify(response["message"])
    else:
        return {}
      
