import sqlite3
import random
import datetime
#what to do in exists if name and id
class Room:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "rooms"
    
    def initialize_rooms_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id TEXT PRIMARY KEY UNIQUE,
                    seats INTEGER
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create_room(self, room_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            room_number = room_info["id"]
            if self.exists(id = room_number)["message"]:
                return {
                        "result": "error",
                        "message": "room already exists"
                    }

            room_data = (room_number, room_info["seats"])
            # print(type(room_data), type(room_data[1]))
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?);", room_data)
            db_connection.commit()
        
            return {"result": "success",
                    # "message": "help"
                    "message": self.get_room(id = room_number)["message"]
                    }
     
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_room(self, id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if id != None:
                if self.exists(id = id)["message"]:
                    query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = '{id}';"
                else:
                    return {"result":"error",
                            "message":"id doesn't exist"}
                
            results = cursor.execute(query).fetchall()[0]

            dict = self.to_dict(results)

            return {"result": "success",
                    "message": dict
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def get_rooms(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            rooms = []
            query = f"SELECT * from {self.table_name};"

            results = cursor.execute(query).fetchall()
            print(results)

            for room in results:
                rooms.append(self.to_dict(room))

            return {"result": "success",
                    "message": rooms
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def update_room(self, room_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(id = room_info["id"])["message"] == False:
                return {"result":"error",
                        "message":"room doesn't exist"}
            
           
            query = f"UPDATE {self.table_name} SET seats = '{room_info['seats']}' WHERE id = '{room_info['id']}';"
            
            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": self.get_room(room_info["id"])["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def remove_room(self, id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(id)["message"] == False:
                return {"result":"error",
                        "message":"room doesn't exist"}
        

            room = self.get_room(id)
            # print(user)
            query = f"DELETE FROM {self.table_name} WHERE id = '{id}';"

            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": room["message"]
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
    
    def to_dict(self, room_info):
        dict = {"id": room_info[0],
                "seats": room_info[1],
                }

        
        return dict



