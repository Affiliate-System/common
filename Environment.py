from common.orm import ORM
from common.logging import InfoLogger, ErrorLogger
from config.config import *


class Environment:
    def __init__(self, databaseName):
        self.databaseName = databaseName

    def getPublishTimes(self):
        res = self.__updatePublishTimes()
        if res:
            ErrorLogger.error('Environment.getPublishTimes')
            return None, res

        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.getPublishTimes')
            return None, res

        if PUBLISH_TIMES_KEY not in env.keys():
            ErrorLogger.error(f'Environment.getPublishTimes.{PUBLISH_TIMES_KEY}_not_exist_in_env')
            return None, res

        publishTimes = env[PUBLISH_TIMES_KEY]
        return publishTimes, None

    def updatePublishTimes(self, productId):
        orm = ORM()
        res = orm.connect('', self.databaseName, DB_ENV_TABLE)
        if res:
            ErrorLogger.error('Environment.__getEnvFromDB')
            return None, res

        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.updatePublishTimes')
            return res

        env[PUBLISH_TIMES_KEY][productId] += 1

        query = {'_id': env['_id']}
        data = {PUBLISH_TIMES_KEY: env[PUBLISH_TIMES_KEY]}
        row_count = orm.update(query, data)
        if row_count == 0:
            e = Exception('Environment.updatePublishTimes.fail_update_publish_times')
            ErrorLogger.error(str(e))
            return e

        InfoLogger.info('Environment.updatePublishTimes.success')
        return None

    def updateRecentPublishing(self, productId):
        orm = ORM()
        res = orm.connect('', self.databaseName, DB_ENV_TABLE)
        if res:
            ErrorLogger.error('Environment.updateRecentPublishing')
            return None, res

        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.updateRecentPublishing')
            return res

        query = {'_id': env['_id']}
        data = {RECENT_PUBLISHING_KEY: productId}
        row_count = orm.update(query, data)
        if row_count == 0:
            e = Exception('Environment.updateRecentPublishing.fail_update_publish_times')
            ErrorLogger.error(str(e))
            return e

        InfoLogger.info('Environment.updateRecentPublishing.success')
        return None

    def __getEnvFromDB(self):
        orm = ORM()
        res = orm.connect('', self.databaseName, DB_ENV_TABLE)
        if res:
            ErrorLogger.error('Environment.__getEnvFromDB')
            return None, res

        env, res = orm.find({}, limit=0)
        if res or len(env) < 1:
            ErrorLogger.error('Environment.__getEnvFromDB.empty_or_null_env')
            return None, res

        env = env[0]
        return env, None

    def __updatePublishTimes(self):
        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.__updatePublishTimes')
            return res

        orm = ORM()
        res = orm.connect('', self.databaseName, DB_PRODUCT_TABLE)
        if res:
            ErrorLogger.error('Environment.__updatePublishTimes')
            return res

        products, res = orm.find({}, limit=0)
        if res or len(products) < 1:
            ErrorLogger.error('Environment.__updatePublishTimes.empty_or_null_product_lists')
            return res

        if len(env) == len(products):
            InfoLogger.info('Environment.__updatePublishTimes.env_publish_times_up_to_date')
            return None

        for prod in products:
            productId = str(prod['_id'])
            if productId not in env[PUBLISH_TIMES_KEY].keys():
                env[PUBLISH_TIMES_KEY][productId] = 0

        orm = ORM()
        res = orm.connect('', self.databaseName, DB_ENV_TABLE)
        if res:
            ErrorLogger.error('Environment.__updatePublishTimes')
            return res
        query = {'_id': env['_id']}
        data = {PUBLISH_TIMES_KEY: env[PUBLISH_TIMES_KEY]}
        row_count = orm.update(query, data)
        if row_count == 0:
            e = Exception('Environment.__updatePublishTimes.fail_update_publish_times')
            ErrorLogger.error(str(e))
            return e

        InfoLogger.info('Environment.__updatePublishTimes.success')
        return None
