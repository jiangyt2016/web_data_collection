from ConfigParser import ConfigParser
import log

class Config():
    def __init__(self):
        self.config_file = "config.ini"
        self.result_file = None
        self.url_file = None
        self.host = None
        self.user = None
        self.passwd = None
        self.db = None
        self.parse()

    def parse(self):
        cf = ConfigParser()
        cf.read("config.ini")
        self.result_file = cf.get("result", "file")
        self.url_file = cf.get("url", "file")

        self.host = cf.get("database", host)
        self.user = cf.get("database", user)
        self.passwd = cf.get("database", passwd)
        self.db = cf.get("database", db)


        logger = log.get_logger()
        logger.info("result file:" + self.result_file)
        logger.info("url_file:" + self.url_file)
        logger.info("host:" + self.host)
        logger.info("user:" + self.user)
        logger.info("passwd:" + self.passwd)
        logger.info("db:" + self.db)

def test():
    config = Config()

if __name__ == '__main__':
    test()
