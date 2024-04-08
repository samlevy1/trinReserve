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

def c_rScorecards():
    
    # curl "http://127.0.0.1:5000/scorecards"
    if request.method == "GET":
        response = scorecards.get_scorecards()
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return [] 
        
    elif request.method == "POST":
        #curl -X POST -H "Content-type: application/json" -d '{"user_id":123,"game_id":221334149247354,"turn_order":1}' "http://127.0.0.1:5000/scorecards"
        
        dict = request.json
        response = scorecards.create_scorecard(dict["game_id"],dict["user_id"], dict["turn_order"])
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
             return {}    

def rScorecard_u_d(scorecard_id):
    scorecard_id = int(scorecard_id)
    if request.method == "GET":
        #  curl "http://127.0.0.1:5000/scorecards/1786534531189652118"

        response = scorecards.get_scorecard(scorecard_id)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   

    elif request.method == "PUT":
        #curl -X PUT -H "Content-type: application/json" -d '{"dice_rolls":10,"upper":{"ones":14,"twos":20,"threes":4,"fours":-1,"fives":10,"sixes":-1},"lower":{"three_of_a_kind":20,"four_of_a_kind":-1,"full_house":-1,"small_straight":-1,"large_straight":-1,"yahtzee":-1,"chance":-1}}' "http://127.0.0.1:5000/scorecards/3713127990589409950"

        response = scorecards.update_scorecard(scorecard_id, request.json)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   
 
    elif request.method == "DELETE":
        # curl -X DELETE "http://127.0.0.1:5000/scorecards/1786534531189652118"
        response = scorecards.remove_scorecard(scorecard_id)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   

def getScores():
    # curl "http://127.0.0.1:5000/scores"
    # print("______ERROR HERE____\n")
    all = scorecards.get_scorecards()["message"]
    scores = {}
    highScores = []
    for sc in all:
        scores[str(sc["user_id"]) + "," + str (sc["game_id"])] = sc["score"]

    sorted_scores = sorted(scores.items(), key=lambda x:x[1])

    for score in reversed(sorted_scores):
        ids = score[0].split(",")
        # print(ids)
        # print(ids[0])
        # print(users.get_users())
        # print(users.exists(id = int(ids[0])))
        # print(users.get_user(id = int(ids[0])))
        dict = {
            "score": score[1],
            "username": users.get_user(id = int(ids[0]))["message"]["username"],
            "game_name": games.get_game(id = int(ids[1]))["message"]["name"]
        }
        highScores.append(dict)

    # print(highScores)
    
    if len(highScores) > 10:
        return highScores[0:10]
    else:
        return highScores
        
def getUserScores(username):
    # curl "http://127.0.0.1:5000/scores/cookieM"
    user = users.get_user(username=username)
    if user["result"] == "success":
        id = user["message"]["id"]
    else:
        return [] 

    all = scorecards.get_scorecards()["message"]
    scores = {}
    highScores = []
    for sc in all:
        if sc["user_id"] == id:
            scores[str(sc["user_id"]) + "," + str (sc["game_id"])] = sc["score"]

    sorted_scores = sorted(scores.items(), key=lambda x:x[1])

    for score in reversed(sorted_scores):
        ids = score[0].split(",")
        dict = {
            "score": score[1],
            "username": users.get_user(id = int(ids[0]))["message"]["username"],
            "game_name": games.get_game(id = int(ids[1]))["message"]["name"]
        }
        highScores.append(dict)
        
    # print (highScores)
    return highScores
    
def getGameScorecard(scorecard_id):
    # curl "http://127.0.0.1:5000/scorecards/game/ourGame1"
    sc = scorecards.get_scorecard(int(scorecard_id))

    if sc["result"] == "success":
        game = games.get_game(id = sc["message"]["game_id"])
        return game["message"]
    else:
      return {}