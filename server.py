import tornado.ioloop
import tornado.web
import tornado.httpserver

import os

root = os.path.dirname(__file__)

class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.render("Website/index.html")
        


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/css/(.*)', tornado.web.StaticFileHandler,{"path":'./Website/css'},),
            (r'/js/(.*)', tornado.web.StaticFileHandler,{"path":'./Website/js'},),
            (r'/img/(.*)', tornado.web.StaticFileHandler,{"path":'./Website/img'},),
        ]
        settings = {
            "static_path": os.path.join(root, "Website")

        }
        tornado.web.Application.__init__(self, handlers)

http_server = tornado.httpserver.HTTPServer(Application())
http_server.listen(8888)

if __name__ == "__main__":
    
    tornado.ioloop.IOLoop.instance().start()
