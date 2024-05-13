import sqlite3
import random
import datetime
import json
#what to do in exists if name and id
class Leader:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "leaders"
    

    def initialize_leaders_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    club_id INTEGER,
                    user_id TEXT
                    
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create_leader(self, club_id, user_id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
    
            leader_id = random.randint(0, 9007199254740991) #non-negative range of SQLITE3 INTEGER

            # check to see if exists already!!

            while self.exists(id = leader_id)["message"]:
                leader_id = random.randint(0, 9007199254740991)

          

            leader_data = (leader_id, club_id, user_id)
            
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?);", leader_data)
            db_connection.commit()
        
            return {"result": "success",
                    "message": self.get_leader(leader_id)["message"]
                    }
     
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_leader(self, id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if id != None:
                if self.exists(id = id)["message"]:
                    query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {id};"
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

    def get_leaders(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            leaders = []
            query = f"SELECT * from {self.table_name};"

            results = cursor.execute(query).fetchall()

            for leader in results:
                leaders.append(self.to_dict(leader))
      
            return {"result": "success",
                    "message": leaders
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def remove_leader(self, id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(id)["message"] == False:
                return {"result":"error",
                        "message":"leader doesn't exist"}
        

            leader = self.get_leader(id)
            # print(user)
            query = f"DELETE FROM {self.table_name} WHERE id = {id};"

            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": leader["message"]
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
    
    def to_dict(self, leader_info):
        dict = {"id": leader_info[0],
                "club_id": leader_info[1],
                "user_id": leader_info[2],
                }

        
        return dict
    

    def get_clubLeaders(self, club_id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            leaders = []
            query = f"SELECT * from {self.table_name} WHERE club_id = '{club_id}';"

            results = cursor.execute(query).fetchall()

            for leader in results:
                leaders.append(self.to_dict(leader))
      
            return {"result": "success",
                    "message": leaders
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def get_leaderClubs(self, user_id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            clubs = []
            query = f"SELECT * from {self.table_name} WHERE user_id = '{user_id}';"

            results = cursor.execute(query).fetchall()

            for club in results:
                clubs.append(self.to_dict(club))
        
            return {"result": "success",
                    "message": clubs
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()