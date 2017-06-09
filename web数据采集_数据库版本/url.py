import log

class URL():
    def __init__(self, url_file):
        self.logger = log.get_logger()
        self.logger.info(url_file)
        self.number = 0
        self.url_file = url_file
        self.open_flag = False
        self.fp = None

    def get_count(self):
        count = 0
        try:
            fp = open(self.url_file, "r")
        except Exception:
            return count
        while True:
            line = fp.readline()
            line = line.strip()
            if not line:
                break
            count += 1
        return count


    def get_next(self):
        exp_flag = False
        if self.open_flag == False:
            try:
                self.fp = open(self.url_file, "r")
            except Exception, error_message:
                exp_flag = True
                self.logger.error(error_message)
                self.fp.close()
                self.fp = None
        if self.open_flag == False and exp_flag == False:
            self.open_flag = True
        elif self.open_flag == False and exp_flag == True:
            return False, None
        
        line = self.fp.readline()
        url = None
        if not line:
            url = None
            self.fp.close()
        else:
            url = line.strip()
        return True, url

def test():
    url = URL("url.txt")
    print url.get_next()
    print url.get_next()
    print url.get_next()

if __name__ == '__main__':
    test()

