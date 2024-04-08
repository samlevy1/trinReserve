import sqlite3
import random
import datetime
#what to do in exists if name and id
class Game:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "games"
    
    def initialize_games_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    name TEXT UNIQUE,
                    link TEXT UNIQUE,
                    created TIMESTAMP,
                    finished TIMESTAMP
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create_game(self, game_details):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(name = game_details["name"])["message"]:
                return {
                        "result": "error",
                        "message": "name already exists"
                    }

            game_id = random.randint(0, 9007199254740991) #non-negative range of SQLITE3 INTEGER
            game_link = random.randint(0, 9007199254740991)
            # check to see if exists already!!

            while self.exists(id = game_id)["message"]:
                game_id = random.randint(0, 9007199254740991)
            while self.exists(link = game_link)["message"]:
                game_link = random.randint(0, 9007199254740991)

            game_details["link"] = str(game_link)


            # #username & email checks
            if game_details["name"].isalnum() == False or game_details["link"].isalnum() == False:
                return {
                        "result": "error",
                        "message": "name formatted wrong"
                    }

            created = datetime.datetime.now()
            game_data = (game_id, game_details["name"], game_details["link"], created, created)
            
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?);", game_data)
            db_connection.commit()
        
            return {"result": "success",
                    "message": self.get_game(name = game_details["name"])["message"]
                    }
     
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_game(self, id = None, name = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if id != None:
                if self.exists(id = id)["message"]:
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

    def get_games(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            games = []
            query = f"SELECT * from {self.table_name};"

            results = cursor.execute(query).fetchall()
            print(results)

            for game in results:
                games.append(self.to_dict(game))
      
            return {"result": "success",
                    "message": games
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def update_game(self, game_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(id = game_info["id"])["message"] == False:
                return {"result":"error",
                        "message":"id doesn't exist"}
            
            if "finished" in game_info.keys():
                query = f"UPDATE {self.table_name} SET name = '{game_info['name']}', link = '{game_info['link']}', finished = '{game_info['finished']}' WHERE id = {game_info['id']};"
            else:
                query = f"UPDATE {self.table_name} SET name = '{game_info['name']}', link = '{game_info['link']}' WHERE id = {game_info['id']};"
            
            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": self.get_game(game_info["id"])["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def remove_game(self, name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(name=name)["message"] == False:
                return {"result":"error",
                        "message":"game doesn't exist"}
        

            game = self.get_game(name = name)
            # print(user)
            query = f"DELETE FROM {self.table_name} WHERE name = '{name}';"

            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": game["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def is_finished(self, name):
        game = self.get_game(name = name)["message"]

        if game["created"] != game["finished"]:
            return {"result": "success",
                    "message": True
                    }
        else:
            return {"result": "success",
                    "message": False
                    }

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
    
    def to_dict(self, game_info):
        dict = {"id": game_info[0],
                "name": game_info[1],
                "link": game_info[2],
                "created": game_info[3],
                "finished": game_info[4]
                }

        
        return dict



