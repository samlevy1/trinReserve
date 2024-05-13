from flask import jsonify
from flask import request
import os
import sys

fpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
sys.path.insert(0,fpath)

from models import UsersModel
from models import ClubsModel
from models import RoomsModel
# from db_server.models import ClubsModel
# from db_server.models import ClubLeadersModels
# from UsersModel import *
# from GamesModel import *
# from ScorecardsModel import *

trinReserve_db_name=f"{os.getcwd()}/models/trinReserveDB.db"


users = UsersModel.User(trinReserve_db_name)
clubs = ClubsModel.Club(trinReserve_db_name)
rooms = RoomsModel.Room(trinReserve_db_name)
# scorecards = ClubLeadersModels.Scorecard(yahtzee_db_name)

def c_rRooms():
    
    # curl "http://127.0.0.1:5000/rooms"
    if request.method == "GET":
        response = rooms.get_rooms()
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
            # return [] 
        
    elif request.method == "POST":
        #curl -X POST -H "Content-type: application/json" -d '{"id":"N302", "seats": 10}' "http://127.0.0.1:5000/rooms"
        # return jsonify(request.json)
        response = rooms.create_room(request.json)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
            # return {} 
    
def rRoom_u_d(room_id):
    if request.method == "GET":
        #  curl "http://127.0.0.1:5000/rooms/testroom"
        # print(room_id)
        response = rooms.get_room(id = room_id)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   

    elif request.method == "PUT":
        #curl -X PUT -H "Content-type: application/json" -d '{"id": "N302", "seats": 15 }' "http://127.0.0.1:5000/rooms/N302"

        response = rooms.update_room(request.json)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
        #     return {}   
 
    elif request.method == "DELETE":
        # curl -X DELETE "http://127.0.0.1:5000/rooms/N301"
        response = rooms.remove_room(room_id)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
            # return {}   
            
