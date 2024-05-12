import sqlite3
import random
import datetime
import json
#what to do in exists if name and id
class Meeting:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "meetings"
    

    def initialize_meetings_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    date DATE,
                    club_id INTEGER,
                    room_id TEXT,
                    meeting_description TEXT,
                    seats_left INTEGER,
                    attendees INTEGER
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create_meeting(self, meeting_info):
        print(meeting_info)
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            meeting_id = random.randint(0, 9007199254740991) #non-negative range of SQLITE3 INTEGER
            
            # check to see if exists already!!
            if self.get_clubDateMeeting(meeting_info["club_id"], meeting_info["date"]):
                return {"result": "error",
                    "message": "meeting already exists"
                    }
        

            while self.exists(id = meeting_id)["message"]:
                meeting_id = random.randint(0, 9007199254740991)


            meeting_data = (meeting_id, meeting_info["date"], meeting_info["club_id"], meeting_info["room_id"], meeting_info["meeting_description"], meeting_info["seats_left"], meeting_info["attendees"])
            
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?, ?, ?);", meeting_data)
            db_connection.commit()
        
            return {"result": "success",
                    "message": self.get_meeting(meeting_id)["message"]
                    }
     
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_meeting(self, id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            if id != None:
                if self.exists(id = int(id))["message"]:
                    query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {id};"
                else:
                    return {"result":"error",
                            "message":"id doesn't exist"}
            
            results = cursor.execute(query).fetchall()[0]

            dict = self.to_dict(results)
            print(dict)
            return {"result": "success",
                    "message": dict
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def get_meetings(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            meetings = []
            query = f"SELECT * from {self.table_name};"

            results = cursor.execute(query).fetchall()

            for meeting in results:
                meetings.append(self.to_dict(meeting))
      
            return {"result": "success",
                    "message": meetings
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def update_meeting(self, meeting_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(meeting_info["id"])["message"] == False:
                return {"result":"error",
                        "message":"id doesn't exist"}
            #  room_id = '{meeting_info["room_id"]}', meeting_description = '{meeting_info["meeting_description"]}', seats_left = '{meeting_info["seats_left"]}', attendees = '{meeting_info["attendees"]}'
            query = f"UPDATE {self.table_name} SET date = '{meeting_info['date']}', room_id = '{meeting_info['room_id']}', meeting_description = '{meeting_info['meeting_description']}' , seats_left = '{meeting_info['seats_left']}', attendees = '{meeting_info['attendees']}'  WHERE id = '{meeting_info['id']}';"
                    
            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": self.get_meeting(meeting_info["id"])["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def remove_meeting(self, id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(id)["message"] == False:
                return {"result":"error",
                        "message":"game doesn't exist"}
        

            meeting = self.get_meeting(id)
            # print(user)
            query = f"DELETE FROM {self.table_name} WHERE id = {id};"

            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": meeting["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def exists(self, id):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            exist = False
            id = int(id)
            if id != None:
                ids = cursor.execute(f"SELECT id from {self.table_name} ;").fetchall()       


                for i in ids:
                    if id == i[0]:
                        exist = True

            return {"result": "success",
                    "message": exist
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

        return exist
    
    def to_dict(self, meeting_info):
        dict = {"id": meeting_info[0],
                "date": meeting_info[1],
                "club_id": meeting_info[2],
                "room_id": meeting_info[3],
                "meeting_description": meeting_info[4],
                "seats_left": meeting_info[5],
                "attendees": meeting_info[6]
                }

        
        return dict
    
    def get_roomMeetings(self, room_id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            meetings = []
            query = f"SELECT * from {self.table_name} WHERE room_id = '{room_id}';"

            results = cursor.execute(query).fetchall()

            for meeting in results:
                meetings.append(self.to_dict(meeting))
        
            return {"result": "success",
                    "message": meetings
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def get_clubMeetings(self, club_id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            meetings = []
            query = f"SELECT * from {self.table_name} WHERE club_id = '{club_id}';"

            results = cursor.execute(query).fetchall()

            for meeting in results:
                meetings.append(self.to_dict(meeting))
        
            return {"result": "success",
                    "message": meetings
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
            
    def get_dateMeetings(self, date):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            meetings = []
            query = f"SELECT * from {self.table_name} WHERE date = '{date}';"

            results = cursor.execute(query).fetchall()

            for meeting in results:
                meetings.append(self.to_dict(meeting))
        
            return {"result": "success",
                    "message": meetings
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()        
   
    def get_clubDateMeeting(self, club_id, date):
            try: 
                db_connection = sqlite3.connect(self.db_name)
                cursor = db_connection.cursor()

                meetings = []
                query = f"SELECT * from {self.table_name} WHERE date = '{date}' AND club_id = '{club_id}';"

                results = cursor.execute(query).fetchall()

                for meeting in results:
                    meetings.append(self.to_dict(meeting))
            
                return {"result": "success",
                        "message": meetings
                        }
            
            except sqlite3.Error as error:
                return {"result":"error",
                        "message":error}
            
            finally:
                db_connection.close() 

    def add_attendee(self, id):
            try: 
                db_connection = sqlite3.connect(self.db_name)
                cursor = db_connection.cursor()

                if self.exists(id)["message"] == False:
                    return {"result":"error",
                            "message":"id doesn't exist"}
                
                attendees = self.get_meeting(id)["message"]["attendees"] + 1
                
                query = f"UPDATE {self.table_name} SET attendees = '{attendees}' WHERE id = {id};"
                
                results = cursor.execute(query)

                db_connection.commit()

                return {"result": "success",
                        "message": self.get_meeting(id)["message"]
                        }
            
            except sqlite3.Error as error:
                return {"result":"error",
                        "message":error}
            
            finally:
                db_connection.close()