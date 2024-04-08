import sqlite3
import random
import datetime
import json
#what to do in exists if name and id
class Scorecard:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "scorecards"
    

    def initialize_scorecards_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    game_id INTEGER,
                    user_id INTEGER,
                    score_info TEXT,
                    turn_order INTEGER,
                    score INTEGER
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create_scorecard(self, game_id, user_id, order):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            gameScorecards = self.get_game_scorecards(game_id)["message"]  

            # print(gameScorecards)
            if len(gameScorecards) >= 4:
                 return {"result":"error",
                    "message":"too many scorecards"}
            if len(gameScorecards) > 0:
                for card in gameScorecards:

                    if card["user_id"] == user_id:
                        return {"result":"error",
                        "message":"user already has scorecard"}
                    
            scorecard_id = random.randint(0, 9007199254740991) #non-negative range of SQLITE3 INTEGER

            # check to see if exists already!!

            while self.exists(id = scorecard_id)["message"]:
                scorecard_id = random.randint(0, 9007199254740991)

            score_info = {
            "dice_rolls":3,
            "upper":{
                "ones":-1,
                "twos":-1,
                "threes":-1,
                "fours":-1,
                "fives":-1,
                "sixes":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
            }
            score_info = json.dumps(score_info)
            score = 0

            scorecard_data = (scorecard_id, game_id, user_id, score_info, order, score)
            
            cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?, ?, ?);", scorecard_data)
            db_connection.commit()
        
            return {"result": "success",
                    "message": self.get_scorecard(scorecard_id)["message"]
                    }
     
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_scorecard(self, id):
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

    def get_scorecards(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            scorecards = []
            query = f"SELECT * from {self.table_name};"

            results = cursor.execute(query).fetchall()

            for scorecard in results:
                scorecards.append(self.to_dict(scorecard))
      
            return {"result": "success",
                    "message": scorecards
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def get_game_scorecards(self, game_id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            scorecards = []
            query = f"SELECT * from {self.table_name} WHERE game_id = '{game_id}';"

            results = cursor.execute(query).fetchall()

            for scorecard in results:
                scorecards.append(self.to_dict(scorecard))
      
            return {"result": "success",
                    "message": scorecards
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def update_scorecard(self, id, score_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(id)["message"] == False:
                return {"result":"error",
                        "message":"id doesn't exist"}
            
            score = self.tally_score(score_info)
            score_info = json.dumps(score_info)
            query = f"UPDATE {self.table_name} SET score_info = '{score_info}', score = {score} WHERE id = {id};"
            
            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": self.get_scorecard(id)["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def remove_scorecard(self, id):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            if self.exists(id)["message"] == False:
                return {"result":"error",
                        "message":"game doesn't exist"}
        

            scorecard = self.get_scorecard(id)
            # print(user)
            query = f"DELETE FROM {self.table_name} WHERE id = {id};"

            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": scorecard["message"]
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
    
    def to_dict(self, scorecard_info):
        dict = {"id": scorecard_info[0],
                "game_id": scorecard_info[1],
                "user_id": scorecard_info[2],
                "score_info": json.loads(scorecard_info[3]),
                "turn_order": scorecard_info[4],
                "score": scorecard_info[5]
                }

        
        return dict
    
    def tally_score(self, score_info):
        score = 0
        for key in score_info:
            if key != "dice_rolls":
                for roll in score_info[key]:
                    if score_info[key][roll] != -1:
                        score +=score_info[key][roll]

        return score

