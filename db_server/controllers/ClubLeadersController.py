from flask import jsonify
from flask import request
import os
import sys

fpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
sys.path.insert(0,fpath)

from models import UsersModel
from models import ClubsModel
from models import ClubLeadersModel

# from db_server.models import ClubLeadersModels
# from UsersModel import *
# from GamesModel import *
# from ScorecardsModel import *

trinReserve_db_name=f"{os.getcwd()}/models/trinReserveDB.db"


users = UsersModel.User(trinReserve_db_name)
clubs = ClubsModel.Club(trinReserve_db_name)
leaders = ClubLeadersModel.Leader(trinReserve_db_name)
# scorecards = ClubLeadersModels.Scorecard(yahtzee_db_name)


def c_rLeaders():
    
    # curl "http://127.0.0.1:5000/leaders"
    if request.method == "GET":
        response = leaders.get_leaders()
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return [] 
        
    elif request.method == "POST":
        #curl -X POST -H "Content-type: application/json" -d '{"user_id":12345,"club_id":3123}' "http://127.0.0.1:5000/leaders"
        
        dict = request.json
        print(dict["club_id"],dict["user_id"])
        response = leaders.create_leader(dict["club_id"],dict["user_id"])
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
             return {}    

def r_dLeader(leader_id):
    leader_id = int(leader_id)

    if request.method == "DELETE":
        # curl -X DELETE "http://127.0.0.1:5000/leaders/8281298765910965"
        response = leaders.remove_leader(leader_id)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   
        
    elif request.method == "GET":
        #  curl "http://127.0.0.1:5000/leaders/7687158050316891"
        print(leader_id)
        response = leaders.get_leader(leader_id)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {} 


def getleaderClubs(leader_id):
    # curl "http://127.0.0.1:5000/leaderClubs/12345"
    print(leader_id)

    response = leaders.get_leaderClubs(leader_id)
    if response["result"] == "success":
        return jsonify(response["message"])
    else:
        return {} 
    
def getClubLeaders(club_id):
    # curl "http://127.0.0.1:5000/clubLeaders/221334149247354"
    print(club_id)

    response = leaders.get_clubLeaders(club_id)
    if response["result"] == "success":
        return jsonify(response["message"])
    else:
        return {} 