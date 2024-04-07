# This file takes care of creating a table, updating and retrieving records for the transactions
# FACTS TABLE structure = {{"date": str, "message": str, "suggest_nd": str, "approve_nd": bool, "update_dt": str}}
# Primary Composite key is a combination of "date" and "message" fields, which is a fact.
# The Column approve_nd is updated to True if the fact is approved or False.
# The suggest_nd is the indicator which specifies whether the fact was added or removed or changed.
# The update_dt stored the time stamp at which the row is updated.
# Only the facts which are approved are shown to the users and have updated in last 24 hours are shown.

from sqlite_utils import Database
import sqlite3
from datetime import datetime

db = Database(sqlite3.connect("summariser.db", check_same_thread=False))


class DatabaseClass:
    def __init__(self) -> None:
        self.db = db

    def create_db_details(self, input):
        self.db["facts"].create(
            {
                "date": str,
                "message": str,
                "suggest_nd": str,
                "approve_nd": bool,
                "update_dt": str,
            },
            pk=("date", "message"),
            replace=True,
        )
        self.db["facts"].insert_all(input)

    def update_table(self, new_list):
        for val in new_list:
            self.db["facts"].update(
                (val[0], val[1]), {"approve_nd": val[2], "update_dt": val[3]}
            )
        for row in self.db["facts"].rows:
            print(row)

    def get_allvalues(self):
        return self.db["facts"].rows
