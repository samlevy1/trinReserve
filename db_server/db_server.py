#sofia zhang 11-1
from flask import Flask
from flask import request
from flask import jsonify
import os
import sys

from db_server.controllers import ClubsController, clubLeadersController

fpath = os.path.join(os.path.dirname(__file__), 'controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'models')
sys.path.append(fpath)

from controllers import UsersController

app = Flask(__name__, static_url_path='', static_folder='static')

def welcome():

    return """
           <html>
           <head>
             <link rel="stylesheet" href="styles.css">
           </head>
           <body>
             <h1>Welcome!</h1>
           </body>
           </html>
            """
app.add_url_rule('/', view_func=welcome)

#users
app.add_url_rule('/users', view_func=UsersController.c_rUsers, methods = ["GET", "POST"])
app.add_url_rule('/users/<user_name>', view_func=UsersController.rUser_u_d, methods = ["GET", "PUT", "DELETE"])
app.add_url_rule('/users/id/<id>', view_func=UsersController.get_user_id)
app.add_url_rule('/users/games/<user_name>', view_func=UsersController.get_user_games)


# #games
app.add_url_rule('/games', view_func=ClubsController.c_rGames, methods = ["GET", "POST"])
app.add_url_rule('/games/<game_name>', view_func=ClubsController.rGame_u_d, methods = ["GET", "PUT", "DELETE"])
app.add_url_rule('/games/scorecards/<game_name>', view_func=ClubsController.get_game_scs)

# #scorecards
app.add_url_rule('/scores', view_func=clubLeadersController.getScores)
app.add_url_rule('/scores/<username>', view_func=clubLeadersController.getUserScores)
app.add_url_rule('/scorecards', view_func=clubLeadersController.c_rScorecards, methods = ["GET", "POST"])
app.add_url_rule('/scorecards/<scorecard_id>', view_func=clubLeadersController.rScorecard_u_d, methods = ["GET", "PUT", "DELETE"])
app.add_url_rule('/scorecards/game/<scorecard_id>', view_func=clubLeadersController.getGameScorecard)


app.run(debug=True, port=5000)