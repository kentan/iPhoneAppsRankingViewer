import icon_getter;
import model;
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from xml.dom import minidom

class MainPage(webapp.RequestHandler):
    def get(self):
        
        ig = icon_getter.IconGetter();

        for key in model.AppDef.dbModels:
            appEntry = model.AppDef.dbModels.get(key);
#            appEntryHistory = model.AppDef.dbHistoryModels.get(key);
            
            q = appEntry.all();
            q.filter("rank =", 0)
            results = q.fetch(10);
            for item in results:

                iconUrl = ig.getIcon(item.url);
                item.iconUrl= iconUrl;
                item.put();
                self.response.out.write(item.iconUrl);
                self.response.out.write("</br>");   
                     
application = webapp.WSGIApplication([('/.*', MainPage)], debug=True)
run_wsgi_app(application)
