import pymongo

from common.logging import InfoLogger, ErrorLogger, InfoLogger


class ORM:
    def __init__(self):
        self.table = None

    def connect(self, uri, db_name, table_name):
        try:
            client = pymongo.MongoClient(uri)
            db = client[db_name]
            self.table = db[table_name]

        except Exception as e:
            ErrorLogger.error(f'orm.connect.connection_fail. Details: {str( {"uri": uri, "db_name": db_name, "table_name": table_name, "error": e} )}')
            return e

        InfoLogger.info(f'orm.connect.success. Details: {str( {"uri": uri, "db_name": db_name, "table_name": table_name} )}')
        return None

    def find(self, obj, limit=1):
        try:
            items = self.table.find(obj, limit=limit)
            docs = [i for i in items]

        except Exception as e:
            ErrorLogger.error(f'orm.find.fail. Details: {str({"obj": obj, "limit": limit, "error": e})}')
            return e

        InfoLogger.info(f'orm.find.success. Details: {str({"obj": obj, "limit": limit})}')
        return docs, None

    def insert(self, objs):
        try:
            result = self.table.insert_many(objs)

        except Exception as e:
            ErrorLogger.error(f'orm.insert.fail. Details: {str({"objs": objs, "error": e})}')
            return e

        InfoLogger.info(f'orm.insert.success. Details: {str({"objs": objs})}')
        return result.inserted_ids, None

    def update(self, query, data):
        try:
            result = self.table.update_many(query, {"$set": data})

        except Exception as e:
            ErrorLogger.error(f'orm.update.fail. Details: {str({"query": query, "data": data, "error": e})}')
            return e

        InfoLogger.info(f'orm.update.success. Details: {str({"query": query, "data": data})}')
        return result.modified_count, None
