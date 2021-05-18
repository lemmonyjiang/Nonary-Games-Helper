import os
import json
import tornado.ioloop
import tornado.web
from itertools import combinations as combin

class NineHelper:
    participants = [i+1 for i in range(9)]
    """
    Convert a str list to int list.
    e.g. ['1','2','3'] -> [1,2,3]
    """
    @classmethod
    def to_int(cls, str_list):
        #return map(lambda x: int(x), str_list)
        return [int(x) for x in str_list]

    """
    Convert a number to digit(int) list.
    e.g. 123 -> [1,2,3]
    """
    @classmethod
    def to_list(cls, number):
        digits = []
        digits.append(number % 10)
        remain = number // 10
        while remain > 0:
            digits.append(remain % 10)
            remain = remain // 10
        return digits
        pass

    @classmethod
    def calc_root(cls, participants):
        if len(participants) > 0:
            parts = cls.to_int(participants)
            s = sum(parts)
            while s >= 10:
                s = cls.calc_root(cls.to_list(s))
            return s
        else:
            return 0

    @classmethod
    def list_parts(cls, door, participants):
        _door = int(door)
        ret = []
        num = 3
        while num <= 5:
            for c in combin(participants, num):
                if cls.calc_root(c) == _door:
                    line = {}
                    line['fit'] = c
                    line['fit_root'] = door
                    line['left'] = [p for p in participants if p not in c]
                    line['left_root'] = cls.calc_root(line['left'])
                    ret.append(line)
            num += 1
        return ret

    @classmethod
    def get_participants(cls):
        return cls.participants
    
    @classmethod
    def update_participants(cls, parts):
        cls.participants = cls.to_int(parts)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        self.render("templates/index.html", title="Helper for <<Zero Escape: 999>>", parts=NineHelper.get_participants())

class BaseRequestHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.body = json.loads(self.request.body)
        pass

class CalcRootHandler(BaseRequestHandler):
    def post(self):
        parts = self.body.get('participants')
        NineHelper.update_participants(parts)
        self.write(dict(root=NineHelper.calc_root(parts)))

class ListPartsHandler(BaseRequestHandler):
    def post(self):
        parts_list = NineHelper.list_parts(self.body.get('door'), self.body.get('participants'))
        # print(parts_list)
        ret = dict(door=self.body.get('door'), html=self.render_string('templates/parts_list.html', parts_list=parts_list).decode())
        self.write(ret)
        pass

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    # "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    # "login_url": "/login",
    # "xsrf_cookies": True,
    "debug": True,
}
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/calc_root", CalcRootHandler),
    (r"/list_parts", ListPartsHandler)
    # (r"/(apple-touch-icon\.png)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], **settings)

if __name__ == "__main__":
    application.listen(18888)
    tornado.ioloop.IOLoop.current().start()