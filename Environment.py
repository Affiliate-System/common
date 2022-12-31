from common.orm import ORM
from common.logging import InfoLogger, ErrorLogger
from config.config import *

from datetime import datetime


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
            return res

        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.updatePublishTimes')
            return res

        env[PUBLISH_TIMES_KEY][productId] = datetime.utcnow()

        query = {'_id': env['_id']}
        data = {PUBLISH_TIMES_KEY: env[PUBLISH_TIMES_KEY]}
        row_count = orm.update(query, data)
        if row_count == 0:
            e = Exception('Environment.updatePublishTimes.fail_update_publish_times')
            ErrorLogger.error(str(e))
            return e

        InfoLogger.info('Environment.updatePublishTimes.success')
        return None

    def getRecentPublishing(self):
        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.getRecentPublishing')
            return None, res

        if RECENT_PUBLISHING_KEY not in env.keys():
            ErrorLogger.error(f'Environment.getRecentPublishing.{RECENT_PUBLISHING_KEY}_not_exist_in_env')
            return None, res

        recentPublishing = env[RECENT_PUBLISHING_KEY]
        return recentPublishing, None

    def updateRecentPublishing(self, productId):
        orm = ORM()
        res = orm.connect('', self.databaseName, DB_ENV_TABLE)
        if res:
            ErrorLogger.error('Environment.updateRecentPublishing')
            return res

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

    def getEmailFacebook(self):
        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.getEmailFacebook')
            return None, res

        if EMAIL_FACEBOOK_KEY not in env.keys():
            ErrorLogger.error(f'Environment.getEmailFacebook.{EMAIL_FACEBOOK_KEY}_not_exist_in_env')
            return None, res

        emailFacebook = env[EMAIL_FACEBOOK_KEY]
        return emailFacebook, None

    def getPasswordFacebook(self):
        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.getPasswordFacebook')
            return None, res

        if PASSWORD_FACEBOOK_KEY not in env.keys():
            ErrorLogger.error(f'Environment.getPasswordFacebook.{PASSWORD_FACEBOOK_KEY}_not_exist_in_env')
            return None, res

        passFacebook = env[PASSWORD_FACEBOOK_KEY]
        return passFacebook, None

    def getPageNameFacebook(self):
        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.getPageNameFacebook')
            return None, res

        if PAGE_NAME_FACEBOOK_KEY not in env.keys():
            ErrorLogger.error(f'Environment.getPageNameFacebook.{PAGE_NAME_FACEBOOK_KEY}_not_exist_in_env')
            return None, res

        ret = env[PAGE_NAME_FACEBOOK_KEY]
        return ret, None

    def getPageIdFacebook(self):
        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.getPageIdFacebook')
            return None, res

        if PAGE_ID_FACEBOOK_KEY not in env.keys():
            ErrorLogger.error(f'Environment.getPageIdFacebook.{PAGE_ID_FACEBOOK_KEY}_not_exist_in_env')
            return None, res

        ret = env[PAGE_ID_FACEBOOK_KEY]
        return ret, None

    def getViralPageNames(self):
        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.getViralPageNames')
            return None, res

        if VIRAL_PAGE_NAMES_KEY not in env.keys():
            ErrorLogger.error(f'Environment.getViralPageNames.{VIRAL_PAGE_NAMES_KEY}_not_exist_in_env')
            return None, res

        ret = env[VIRAL_PAGE_NAMES_KEY]
        return ret, None

    def getPublishSchedule(self):
        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.getPublishSchedule')
            return None, res

        if PUBLISH_SCHEDULE_KEY not in env.keys():
            ErrorLogger.error(f'Environment.getPublishSchedule.{PUBLISH_SCHEDULE_KEY}_not_exist_in_env')
            return None, res

        ret = env[PUBLISH_SCHEDULE_KEY]
        return ret, None

    def getMarketingSchedule(self):
        env, res = self.__getEnvFromDB()
        if res:
            ErrorLogger.error('Environment.getMarketingSchedule')
            return None, res

        if MARKETING_SCHEDULE_KEY not in env.keys():
            ErrorLogger.error(f'Environment.getMarketingSchedule.{MARKETING_SCHEDULE_KEY}_not_exist_in_env')
            return None, res

        ret = env[MARKETING_SCHEDULE_KEY]
        return ret, None

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
                env[PUBLISH_TIMES_KEY][productId] = datetime.utcnow()

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
