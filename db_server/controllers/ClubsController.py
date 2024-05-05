from flask import jsonify
from flask import request
import os
import sys

fpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
sys.path.insert(0,fpath)

from models import UsersModel
from models import ClubsModel
# from db_server.models import ClubsModel
# from db_server.models import ClubLeadersModels
# from UsersModel import *
# from GamesModel import *
# from ScorecardsModel import *

trinReserve_db_name=f"{os.getcwd()}/models/trinReserveDB.db"


users = UsersModel.User(trinReserve_db_name)
clubs = ClubsModel.Club(trinReserve_db_name)
# scorecards = ClubLeadersModels.Scorecard(yahtzee_db_name)

def c_rClubs():
    
    # curl "http://127.0.0.1:5000/clubs"
    if request.method == "GET":
        response = clubs.get_clubs()
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
            # return [] 
        
    elif request.method == "POST":
        #curl -X POST -H "Content-type: application/json" -d '{"name":"testclub"}' "http://127.0.0.1:5000/clubs"
        # return jsonify(request.json)
        response = clubs.create_club(request.json)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
            # return {} 
    
def rClub_u_d(name_id):
    if request.method == "GET":
        #  curl "http://127.0.0.1:5000/clubs/testclub"
        print(name_id)
        response = clubs.get_club(name = name_id)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   

    elif request.method == "PUT":
        #curl -X PUT -H "Content-type: application/json" -d '{"name": "newClub", "id": 6153875186766167 }' "http://127.0.0.1:5000/clubs/testclub"

        response = clubs.update_club(request.json)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
        #     return {}   
 
    elif request.method == "DELETE":
        # curl -X DELETE "http://127.0.0.1:5000/clubs/newClub"
        response = clubs.remove_club(name_id)
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
      

