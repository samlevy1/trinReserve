from flask import jsonify
from flask import request
import os
import sys

fpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
sys.path.insert(0,fpath)

from models import UsersModel
from db_server.models import ClubsModel
from db_server.models import ClubLeadersModels

yahtzee_db_name=f"{os.getcwd()}/models/yahtzeeDB.db"


users = UsersModel.User(yahtzee_db_name)
games = ClubsModel.Game(yahtzee_db_name)
scorecards = ClubLeadersModels.Scorecard(yahtzee_db_name)

def c_rGames():
    
    # curl "http://127.0.0.1:5000/games"
    if request.method == "GET":
        response = games.get_games()
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
            # return [] 
        
    elif request.method == "POST":
        #curl -X POST -H "Content-type: application/json" -d '{"name":"testGame","link":"Abcd1234"}' "http://127.0.0.1:5000/games"
        # return jsonify(request.json)
        response = games.create_game(request.json)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
            # return {}    

def rGame_u_d(game_name):
    if request.method == "GET":
        #  curl "http://127.0.0.1:5000/games/testGame"
        response = games.get_game(name = game_name)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   

    elif request.method == "PUT":
        #curl -X PUT -H "Content-type: application/json" -d '{"id":6139014500727157862,"name":"ahhhh", "link":"Oand1234", "finished":" 2023-14-25 08:45:06.123837"}' "http://127.0.0.1:5000/games/testGame"
        
        response = games.update_game(request.json)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   
 
    elif request.method == "DELETE":
        # curl -X DELETE "http://127.0.0.1:5000/games/ahhhh"
        response = games.remove_game(game_name)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   


def get_game_scs(game_name):
    # curl "http://127.0.0.1:5000/games/scorecards/ourGame2"
    gameScorecards = []
    game = games.get_game(name = game_name)
    print("working")
    if game["result"] == "success":
        id = game["message"]["id"]
    else:
        return []    
    print("id",id)
    scs = scorecards.get_game_scorecards(id)
    
    return scs["message"]