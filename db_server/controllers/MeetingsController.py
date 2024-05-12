from flask import jsonify
from flask import request
import os
import sys

fpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
sys.path.insert(0,fpath)

from models import UsersModel
from models import MeetingsModel
# from db_server.models import meetingsModel
# from db_server.models import meetingLeadersModels
# from UsersModel import *
# from GamesModel import *
# from ScorecardsModel import *

trinReserve_db_name=f"{os.getcwd()}/models/trinReserveDB.db"


users = UsersModel.User(trinReserve_db_name)
meetings = MeetingsModel.Meeting(trinReserve_db_name)

def c_rMeetings():
    
    # curl "http://127.0.0.1:5000/meetings"
    if request.method == "GET":
        response = meetings.get_meetings()
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
            # return [] 
        
    elif request.method == "POST":

        #curl -X POST -H "Content-type: application/json" -d '{"date":"2008-11-11", "club_id": 222, "room_id": "222", "meeting_description": "help", "seats_left": 10, "attendees": 10}' "http://127.0.0.1:5000/meetings" 
       

        response = meetings.create_meeting(request.json)
        

        if response["result"] == "success":
         return jsonify(response["message"]) 
        else:
         return response["message"]
        

def rMeeting_u_d(meeting_id):
    if request.method == "GET":
        #  curl "http://127.0.0.1:5000/meetings/8778983053005885"

        response = meetings.get_meeting(id = meeting_id)
        if response["result"] == "success":
            return jsonify(response["message"])
        else:
            return {}   

    elif request.method == "PUT":
        #curl -X PUT -H "Content-type: application/json" -d '{"id" : 8778983053005885, "date":"2011-11-11", "club_id": 123, "room_id": "N330", "meeting_description": "new meeting", "seats_left": 10, "attendees": 10}' "http://127.0.0.1:5000/meetings/8778983053005885"

        response = meetings.update_meeting(request.json)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
        #     return {}   
 
    elif request.method == "DELETE":
        # curl -X DELETE "http://127.0.0.1:5000/meetings/8778983053005885"
        response = meetings.remove_meeting(meeting_id)
        # if response["result"] == "success":
        return jsonify(response["message"])
        # else:
            # return {}   

def getRoomMeetings(room_id):
    # curl "http://127.0.0.1:5000/roomMeetings/N325"
    # print(room_id)
    response = meetings.get_roomMeetings(room_id)
    if response["result"] == "success":
        return jsonify(response["message"])
    else:
        return {} 
    
def getClubMeetings(club_id):
    # curl "http://127.0.0.1:5000/clubMeetings/222"

    response = meetings.get_clubMeetings(club_id)
    if response["result"] == "success":
        return jsonify(response["message"])
    else:
        return {} 
    
def getDateMeetings(date):
    # curl "http://127.0.0.1:5000/dateMeetings/2008-11-11"

    response = meetings.get_dateMeetings(date)
    if response["result"] == "success":
        return jsonify(response["message"])
    else:
        return {} 

def getClubDateMeeting(date,club_id):
    #curl "http://127.0.0.1:5000/clubDateMeeting/222/2008-11-11"

    response = meetings.get_clubDateMeeting(club_id,date)
    if response["result"] == "success":
        return jsonify(response["message"])
    else:
        return {}  

def addAttendee(meeting_id):   
     #  curl "http://127.0.0.1:5000/attendee/8978865522329376"

    response = meetings.add_attendee(meeting_id)
    if response["result"] == "success":
        return jsonify(response["message"])
    else:
        return response["message"]