import sqlite3
import random
import datetime
#what to do in exists if name and id
class Club:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "clubs"
    
    def initialize_clubs_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    name TEXT UNIQUE
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create_club(self, club_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            club_name = club_info["name"]
            if self.exists(name = club_name)["message"]:
                return {
                        "result": "error",
                        "message": "name already exists"
                    }

            club_id = random.randint(0, 9007199254740991) #non-negative range of SQLITE3 INTEGER
            
            # check to see if exists already!!

            while self.exists(id = club_id)["message"]:
                club_id = random.randint(0, 9007199254740991)

           
            club_data = (club_id, club_name)
            
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?);", club_data)
            db_connection.commit()
        
            return {"result": "success",
                    "message": self.get_club(name = club_name)["message"]
                    }
     
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_club(self, id = None, name = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if id != None:
                if self.exists(id = int(id))["message"]:
                    query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {id};"
                else:
                    return {"result":"error",
                            "message":"id doesn't exist"}
            elif name != None:
                if self.exists(name=name)["message"]:
                    query = f"SELECT * from {self.table_name} WHERE {self.table_name}.name = '{name}';"
                else:
                    return {"result":"error",
                            "message":"name doesn't exist"}
                
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

    def get_clubs(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            clubs = []
            query = f"SELECT * from {self.table_name};"

            results = cursor.execute(query).fetchall()
            print(results)

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

    def update_club(self, club_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(id = club_info["id"])["message"] == False:
                return {"result":"error",
                        "message":"club doesn't exist"}
            
           
            query = f"UPDATE {self.table_name} SET name = '{club_info['name']}' WHERE id = {club_info['id']};"
            
            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": self.get_club(club_info["id"])["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def remove_club(self, name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(name=name)["message"] == False:
                return {"result":"error",
                        "message":"club doesn't exist"}
        

            club = self.get_club(name = name)
            # print(user)
            query = f"DELETE FROM {self.table_name} WHERE name = '{name}';"

            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": club["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def exists(self, name = None, id = None, link = None):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            exist = False

            if name != None:
                names = cursor.execute(f"SELECT name from {self.table_name} ;").fetchall()
                for n in names:
                    if name == n[0]:
                        exist = True

            elif id != None:
                ids = cursor.execute(f"SELECT id from {self.table_name} ;").fetchall()
                for i in ids:
                    if id == i[0]:
                        exist = True
            
            elif link != None:
                links = cursor.execute(f"SELECT link from {self.table_name} ;").fetchall()
                for l in links:
                    if link == l[0]:
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
    
    def to_dict(self, club_info):
        dict = {"id": club_info[0],
                "name": club_info[1],
                }

        
        return dict



