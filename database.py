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
        results = DB.__cursor.fetchall()
        return results

    def __init__(self):
        if DB.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DB.__instance = self

            DB.__db = connector.connect(
                host='127.0.0.1',
                user='root',
                password='Paulo123',
                database='projeto_pp'
            )

            DB.__cursor = DB.__db.cursor()
