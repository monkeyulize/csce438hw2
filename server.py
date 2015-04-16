import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
from yelpCrawler import *
from twitterCrawler import *
from googleReviews import *
import os

root = os.path.dirname(__file__)
WEBSOCKS = []
class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.render("Website/index.html")
        
class YelpHandler(tornado.websocket.WebSocketHandler):
    
    def open(self):
        
        print("Opened socket")
        
        
    
    def on_message(self, message):
        print("Got message")
        data = json.loads(message);
        yelp = perform_search(data['lat'], data['lng'], data['name']);
        tweets = get_tweets(data['name']);
        greviews = getReviews(data['place_id']);
        if tweets:
            self.write_message('t' + tweets);
        
        if yelp:
            self.write_message('y' + yelp);
        if greviews:
            self.write_message('g' + greviews);
        #print(data['name']);
        
        

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/css/(.*)', tornado.web.StaticFileHandler,{"path":'./Website/css'},),
            (r'/js/(.*)', tornado.web.StaticFileHandler,{"path":'./Website/js'},),
            (r'/img/(.*)', tornado.web.StaticFileHandler,{"path":'./Website/img'},),
            (r'/yelp', YelpHandler),
        ]
        settings = {
            "static_path": os.path.join(root, "Website")

        }
        tornado.web.Application.__init__(self, handlers)

http_server = tornado.httpserver.HTTPServer(Application())
http_server.listen(12345)

if __name__ == "__main__":
    
    tornado.ioloop.IOLoop.instance().start()
