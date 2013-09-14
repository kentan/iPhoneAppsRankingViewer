import icon_getter;
import model;
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from xml.dom import minidom
import urllib2
import datetime
import random
class MainPage(webapp.RequestHandler):
#    def deleteAll(self):
#        for inst in model.AppDef.dbModels.values():
#            q = inst.all(keys_only=True)
#            results = q.fetch(10000)
#            db.delete(results);
#            self.response.out.write("deleted")
#            self.response.out.write("delete comment-outed line for delete !!")

    def putDummyDataToDB(self,entity):

        for index in range(0,100):
            dummyString = "dummy" + str(index);

            dummyRank = random.randint(0,10);
            dummyDate = datetime.date(2013, 3, random.randint(1,31))
            q = entity(title=dummyString,rank=dummyRank,desc=dummyString,date=dummyDate,url="http://google.com",iconUrl="http://a2.mzstatic.com/us/r1000/077/Purple/v4/c2/4f/29/c24f29f4-8d24-b345-7609-085e15a06805/mzl.junlfvwk.png");
            q.put();  
        
        url = "https://itunes.apple.com/jp/rss/topfreeapplications/limit=10/xml";
        response = urllib2.urlopen(url)
        xmlInString = response.read();
        sourceEntry = model.SourceEntry(date=datetime.date.today())
#        key = "topFree";
        for key in model.AppDef.dbModels:
            model.AppDef.dbSourceModels.get(key)(model.AppDef(),sourceEntry,xmlInString);
        response.close();
        sourceEntry.put();
        
    def get(self):
        entity = model.AppDef.dbModels.get("topFree");
        self.putDummyDataToDB(entity);
    def get_backup(self):
        
        ig = icon_getter.IconGetter();

        for key in model.AppDef.dbModels:
            appEntry = model.AppDef.dbModels.get(key);

            
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
