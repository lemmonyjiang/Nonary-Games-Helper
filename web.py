import os
import json
import tornado.ioloop
import tornado.web
from itertools import combinations as combin

class NineHelper:
    @classmethod
    def to_int(cls, str_list):
        return map(lambda x: int(x), str_list)

    @classmethod
    def calc_root(cls, participants):
        if len(participants) > 0:
            parts = cls.to_int(participants)
            s = sum(parts)
            while s >= 10:
                s = cls.calc_root([chr for chr in str(s)])
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

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        self.render("templates/index.html", title="Helper for <<Zero Escape: 999>>")

class BaseRequestHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.body = json.loads(self.request.body)
        pass

class CalcRootHandler(BaseRequestHandler):
    def post(self):
        self.write(dict(root=NineHelper.calc_root(self.body.get('participants'))))

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