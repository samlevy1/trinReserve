import sqlite3
import random

#what to do in exists if username and id

#get all users
#create new user
#get a user from id/email
#updates a single user from id/email
#deletes a single user from id/email

class User:
    def __init__(self, db_name):
        self.db_name =  db_name
        self.table_name = "users"
        print("UsersModel DB loation", self.db_name)


    
    def initialize_users_table(self):
        print("initializing")
        print("UsersModel DB loation", self.table_name)
        db_connection = sqlite3.connect(self.db_name)
        cursor = db_connection.cursor()
        schema=f"""
                CREATE TABLE {self.table_name} (
                    id INTEGER PRIMARY KEY UNIQUE,
                    email TEXT UNIQUE,
                    password TEXT, 
                    administrator TEXT
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

            if self.exists(email=user_details["email"])["message"]:
                result = "error"
                message = "email already exists"

            # check to see if exists already!!
            while self.exists(id = user_id)["message"]:
                user_id = random.randint(0, 9007199254740991)
            
            #email checks
            email = user_details["email"]
            if "@" not in email or email[len(email)-4] != "." or email[len(email)-3:].isalpha() == False:
                result = "error"
                message = "email incorrect format"

            

            pd = user_details["password"]
            if len(pd) < 8 or pd.isupper() == True or pd.islower() == True or pd.isalpha():
                result = "error" 
                message = "password incorrect format"

            user_data = (user_id, user_details["email"], user_details["password"], user_details["administrator"])
            
            # print(user_data)
            # print(self.to_dict(user_data))
            # cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
            if result != "error":
                # are you sure you have all data in the correct format?
                cursor.execute(f"INSERT INTO {self.table_name} VALUES (?, ?, ?, ?);", user_data)
                db_connection.commit()
                print(user_data)
                message = self.to_dict(user_data)
                

            return {
                    "result": result,   
                    "message": message
                    }
     
        
        except sqlite3.Error as error:
            return {"result":"error",
                    "message":error}
        
        finally:
            db_connection.close()
    
    def get_user(self, id = None, email = None):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            
            if id != None:
               
                if self.exists(id = int(id))["message"]:
                    query = f"SELECT * from {self.table_name} WHERE {self.table_name}.id = {int(id)};"
                else:
                    return {"result":"error",
                            "message":"id doesn't exist"}
            elif email != None:
                if self.exists(email=email)["message"]:
                    query = f"SELECT * from {self.table_name} WHERE {self.table_name}.email = '{email}';"
                else:
                    return {"result":"error",
                            "message":"email doesn't exist"}
                
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


            if self.exists(email = user_info["email"])["message"] == False:
                return {"result":"error",
                        "message":"user doesn't exist"}
            id = self.get_user(email=user_info["email"])["message"]["id"]

            query = f"UPDATE {self.table_name} SET email = '{user_info['email']}', password = '{user_info['password']}', administrator = '{user_info['administrator']}' WHERE id = {id};"

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

    def remove_user(self, email):
        try: 
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()

            results = cursor.execute(f"SELECT email FROM {self.table_name}" ).fetchall()
            if self.exists(email=email)["message"] == False:
                return {"result":"error",
                        "message":"email doesn't exist"}
        

            user = self.get_user(email = email)
            # print(user)
            query = f"DELETE FROM {self.table_name} WHERE email = '{email}';"

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

    def exists(self, id = None, email = None):
        try:
            db_connection = sqlite3.connect(self.db_name)
            cursor = db_connection.cursor()
            exist = False

            if id != None:
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
                "password": user_info[2],
                "administrator": user_info[3]
                }
        
        return dict
