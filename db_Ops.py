# CREATE FACTS TABLE (date: date, message : facts, suggestion: (add,delete,remove))
# This file takes care of creating a table, updating and retrieving records for the transactions

from sqlite_utils import Database
import sqlite3
from datetime import datetime
db = Database(sqlite3.connect("summariser.db",check_same_thread=False))

class DatabaseClass():
    def __init__(self) -> None:
        self.db = db

    def create_db_details(self,input):
        self.db["facts"].create({
            "date": str,
            "message": str,
            "suggest_nd": str,
            "approve_nd": bool,
            "update_dt": str
            }, pk=("date","message"), replace=True)
        self.db["facts"].insert_all(input)
    
    def update_table(self,new_list):
        for val in new_list:
            self.db["facts"].update((val[0],val[1]),{"approve_nd": val[2],"update_dt":val[3]})
        for row in self.db["facts"].rows:
            print(row)

    def get_allvalues(self):
        return self.db["facts"].rows