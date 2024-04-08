import sqlite3
import random

#what to do in exists if username and id

class User:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "users"
        print("UsersModel DB loation", self.db_name)


    
    def initialize_users_table(self):
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    email TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT
                )
                """
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")
        results=cursor.execute(schema)
        db_connection.close()
    
    def create_user(self, user_details):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            result = "success"
            user_id = random.randint(0, 9007199254740991) #non-negative range of SQLITE3 INTEGER

            if self.exists(username=user_details["username"])["message"] or self.exists(email=user_details["email"])["message"]:
                result = "error"
                message = "username or email already exists"

            # check to see if exists already!!
            while self.exists(id = user_id)["message"]:
                user_id = random.randint(0, 9007199254740991)
            
            #username & email checks
            email = user_details["email"]
            if user_details["username"].isalnum() == False or "@" not in email or email[len(email)-4] != "." or email[len(email)-3:].isalpha() == False:
                result = "error"
                message = "username or email incorrect format"

            

            pd = user_details["password"]
            if len(pd) < 8 or pd.isupper() == True or pd.islower() == True or pd.isalpha():
                result = "error" 
                message = "password incorrect format"

            user_data = (user_id, user_details["email"], user_details["username"], user_details["password"])
            
            if result != "error":
                #are you sure you have all data in the correct format?
                cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
                db_connection.commit()
                message = self.to_dict(user_data)
            

            return {"result": result,
                    "message": message
                    }
     
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_user(self, id = None, username = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            if id != None:
               
                if self.exists(id = int(id))["message"]:
                    query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {int(id)};"
                else:
                    return {"result":"error",
                            "message":"id doesn't exist"}
            elif username != None:
                if self.exists(username=username)["message"]:
                    query = f"SELECT * from {self.table_name} WHERE {self.table_name}.username = '{username}';"
                else:
                    return {"result":"error",
                            "message":"username doesn't exist"}
                
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

    def get_users(self):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            users = []
            query = f"SELECT * from {self.table_name};"

            results = cursor.execute(query).fetchall()

            for user in results:
                users.append(self.to_dict(user))
      
            return {"result": "success",
                    "message": users
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def update_user(self, user_info):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()


            if self.exists(username = user_info["ogUsername"])["message"] == False:
                return {"result":"error",
                        "message":"user doesn't exist"}
            id = self.get_user(username=user_info["ogUsername"])["message"]["id"]

            query = f"UPDATE {self.table_name} SET email = '{user_info['email']}', username = '{user_info['username']}', password = '{user_info['password']}' WHERE id = {id};"

            # results = cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = {user_info['id']}").fetchall()
            results = cursor.execute(query)

            db_connection.commit()
         
            return {"result": "success",
                    "message": self.get_user(id)["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def remove_user(self, name):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            results = cursor.execute(f"SELECT username FROM {self.table_name}" ).fetchall()
            if self.exists(username=name)["message"] == False:
                return {"result":"error",
                        "message":"username doesn't exist"}
        

            user = self.get_user(username = name)
            # print(user)
            query = f"DELETE FROM {self.table_name} WHERE username = '{name}';"

            results = cursor.execute(query)

            db_connection.commit()

            return {"result": "success",
                    "message": user["message"]
                    }
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()

    def exists(self, username = None, id = None, email = None):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            exist = False

            if username != None:
                usernames = cursor.execute(f"SELECT username from {self.table_name} ;").fetchall()

                for u in usernames:
                    if username == u[0]:
                        exist = True

            elif id != None:
                ids = cursor.execute(f"SELECT id from {self.table_name} ;").fetchall()
                for i in ids:
                    # print(id, i[0])
                    if id == i[0]:
                        exist = True

            elif email != None:
                emails = cursor.execute(f"SELECT email from {self.table_name} ;").fetchall()
                for e in emails:
                    if email == e[0]:
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
    
    def to_dict(self, user_info):
        dict = {"id": user_info[0],
                "email": user_info[1],
                "username": user_info[2],
                "password": user_info[3]
                }
        
        return dict
