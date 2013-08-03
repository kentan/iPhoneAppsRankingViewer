from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
        self.redirect("html/index3.html")      
              
application = webapp.WSGIApplication([('/.*', MainPage)], debug=True)
                
def main():
    run_wsgi_app(application)
