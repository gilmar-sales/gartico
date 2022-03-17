import os
from mysql import connector



# Singleton database class
class DB:
    __instance = None
    __db = None
    __cursor  = None

    @staticmethod
    def getInstance():
        if DB.__instance == None:
            DB()
        return DB.__instance

    def executeQuery(self, query):
        DB.__cursor.execute(query)
        try:
            results = DB.__cursor.fetchall()
            return results
        except Exception as e:
            print(e)
            return
    
    def apply(self):
        DB.__db.commit()

    def validateInput(self, input):
        for char in input:
            if char == '`' or char == '\'' or char == '\"':
                return None
        
        return input

    def __init__(self):
        if DB.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DB.__instance = self

            DB.__db = connector.connect(
                host=os.getenv('DATABASE_HOST'),
                port=os.getenv('DATABASE_PORT', 3306),
                user=os.getenv('DATABASE_USER'),
                password=os.getenv('DATABASE_PASSWORD'),
                database=os.getenv('DATABASE_NAME')
            )

            DB.__cursor = DB.__db.cursor()
