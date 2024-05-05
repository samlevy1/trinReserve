from flask import Flask
from flask import request
from flask import jsonify
import os
import sys

from controllers import UsersController, ClubsController, RoomsController, ClubLeadersController
# from controllers import  ClubsController
print(dir(RoomsController))

# , ClubsController, ClubLeadersController, RoomsController, MeetingsController

fpath = os.path.join(os.path.dirname(__file__), 'controllers')
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'models')
sys.path.append(fpath)

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

# GET /users
# GET /users/<id/email>
# POST /users
# PUT /users/<id/email>
# DELETE /users/<id/email>

# Users
app.add_url_rule('/users', view_func=UsersController.c_rUsers, methods = ["GET", "POST"])
app.add_url_rule('/users/<email_id>', view_func=UsersController.rUser_u_d, methods = ["GET", "PUT", "DELETE"])

# # Clubs
app.add_url_rule('/clubs', view_func=ClubsController.c_rClubs, methods = ["GET", "POST"])
app.add_url_rule('/clubs/<name_id>', view_func=ClubsController.rClub_u_d, methods = ["GET", "PUT", "DELETE"])

# # Leaders
app.add_url_rule('/leaders', view_func=ClubLeadersController.c_rLeaders, methods = ["GET", "POST"])
app.add_url_rule('/leaders/<leader_id>', view_func=ClubLeadersController.r_dLeader,methods = ["GET", "DELETE"])
app.add_url_rule('/clubLeaders/<club_id>', view_func=ClubLeadersController.getClubLeaders)
app.add_url_rule('/leaderClubs/<leader_id>', view_func=ClubLeadersController.getleaderClubs)

# # Rooms
app.add_url_rule('/rooms', view_func=RoomsController.c_rRooms, methods = ["GET", "POST"])
app.add_url_rule('/rooms/<room_id>', view_func=RoomsController.rRoom_u_d, methods = ["GET", "PUT", "DELETE"])

# app.add_url_rule('/room/<id>', view_func=RoomsController.c_rRooms)
# app.add_url_rule('/rooms/<id>', view_func=RoomsController.rClub_u_d,  methods = ["PUT", "DELETE"])

# # Meetings
# app.add_url_rule('/meetings', view_func=MeetingsController.c_rGames, methods = ["GET", "POST"])
# app.add_url_rule('/meetings/<id>/<date.club_id.room_id>', view_func=MeetingsController.c_rGames)
# app.add_url_rule('/meetings/<id>', view_func=MeetingsController.c_rGames, methods = ["PUT", "DELETE"])
# app.add_url_rule('/roomMeetings/<room_id>', view_func=MeetingsController.c_rGames)
# app.add_url_rule('/clubMeetings/<club_id>', view_func=MeetingsController.c_rGames)
# app.add_url_rule('/attendee/<id>', view_func=MeetingsController.c_rGames)

app.run(debug=True, port=5000)