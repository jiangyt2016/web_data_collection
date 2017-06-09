import logging

def get_logger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('log.txt')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
def clear_log():
    fp = open("log.txt", "w")
    fp.close()

def test():
    logger = get_logger()
    clear_log()
    logger.info("aaa")
    logger.error("bbb")

if __name__ == '__main__':
    test()