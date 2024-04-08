from flask import jsonify
from flask import request
import os
import sys

fpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
sys.path.insert(0,fpath)

from models import UsersModel
from db_server.models import ClubsModel
from db_server.models import ClubLeadersModels
# from UsersModel import *
# from GamesModel import *
# from ScorecardsModel import *

yahtzee_db_name=f"{os.getcwd()}/models/yahtzeeDB.db"


users = UsersModel.User(yahtzee_db_name)
games = ClubsModel.Game(yahtzee_db_name)
scorecards = ClubLeadersModels.Scorecard(yahtzee_db_name)

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
        #curl -X POST -H "Content-type: application/json" -d '{"email":"uma.menon@trinityschoolnyc.org","username":"umaM","password":"123TriniT"}' "http://127.0.0.1:5000/users"
        # return jsonify(request.json)
        response = users.create_user(request.json)
        print(f"the response is {response['message']}")
        # if response["result"] == "success":
        return jsonify(response["message"])
        # if response["result"] == "success":
        #     return jsonify(response["message"])
        # else:
        #     return {}    
    
def rUser_u_d(user_name):
    if request.method == "GET":
        #  curl "http://127.0.0.1:5000/users/snowytiger22"
        response = users.get_user(username = user_name)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   

    elif request.method == "PUT":
        #curl -X PUT -H "Content-type: application/json" -d '{"id":2,"email":"snowytiger22@gmail.com", "username":"zhanger", "password":"123TriniT"}' "http://127.0.0.1:5000/users/snowytiger22"

        response = users.update_user(request.json)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
        #     return {}   
 
    elif request.method == "DELETE":
        # curl -X DELETE "http://127.0.0.1:5000/users/justingohde"
        response = users.remove_user(user_name)
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
      
def get_user_games(user_name):
    # curl "http://127.0.0.1:5000/users/games/luigiOfficial"
    # /users/games/<user_name>
    userGames = []
    user = users.get_user(username = user_name)


    if user["result"] == "success":
        id = user["message"]["id"]

    else:
        
        return []    
    print(id)
    scs = scorecards.get_scorecards()

    if scs["result"] == "success":
        for sc in scs["message"]:

            if sc["user_id"] == id:
                gameId = sc["game_id"]
                game = games.get_game(gameId)["message"]
                userGames.append(game)
        # print(jsonify(userGames))
        return jsonify(userGames)
    else:
        return []
    
    
