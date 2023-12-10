from dotenv import dotenv_values
import mysql.connector as con

class DB:
    def __init__(self):  
        try:
            env_var = dotenv_values(".env")
            self.db = con.connect(
                host=env_var.get("host", ""),
                user=env_var.get("user", ""),
                passwd=env_var.get("passwd", ""),
                database="mtxgame"
            )
        except:
            raise "ERROR: Unable to connect to Database."
        self.cr = self.db.cursor()