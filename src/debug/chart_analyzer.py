# -*- coding:utf-8 -*- 
'''
Created on 2013/09/04

@author: kentan
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from xml.dom import minidom
import model
import datetime
import zlib
from datetime import timedelta;
import urllib2
import time;

class MainPage(webapp.RequestHandler):
    def parse_dom(self,xml,searching_app_id,searching_date):
        ranking_history = "";
        dom = minidom.parseString(xml)
        nodeFeed = dom.childNodes[0];
        rank = 0;
        for n in nodeFeed.childNodes:
            if isinstance(n,minidom.Element) and n.nodeName == "entry":

                for n2 in n.childNodes:
#                    print "1</br>"
                    if isinstance(n2,minidom.Element):
                        if n2.nodeName == "id":
#                            print "3</br>"
                            imid = n2.attributes['im:id'].value;
                            if searching_app_id == imid:
#                                print "4</br>"
                                ranking_history += model.rankCode[rank];
                                print str(searching_date) + ":::::" + model.rankCode[rank] + "</br>";
                                break;
                rank += 1
            if(rank >= 61) :break;
        return ranking_history;
    
    def get_ranking_history(self,searching_app_id):
        q = model.RankHistory.all();
        q.filter("appId", int(searching_app_id));
        results = q.fetch(1);
        
        entry = results[0]
        print (entry.topFree) + "</br>";
#        print (entry.topFreeIpad) +"</br>"
        print zlib.decompress(entry.topFree) + "b</br>";
#        print zlib.decompress(entry.topFreeIpad);
    
    def generate_from_source(self,searching_app_id):
        global rankCode;
        ranking_history = {};
        today = datetime.date.today();
        print searching_app_id; 
        DURATION = 100;
        for i in range(0,DURATION):
            time.sleep(1);
            searching_date = today -  timedelta(i)
            print searching_date

            db_name = "SourceEntry";
            q = db.GqlQuery("SELECT * FROM " + db_name +" where date = DATE('" + str(searching_date) + "') ");

            results = q.fetch(1);
            if len(results) == 0:
                continue;

            entry = results[0];
            entry_rank_history = model.RankHistory();
            entry_rank_history.appId = int(searching_app_id) 
            for key in model.AppDef.urls.keys():

                print key;
                compressed_xml = getattr(entry,key);
                if compressed_xml == None:
                    continue;
                xml = zlib.decompress(compressed_xml); 
#                print xml;
#                ranking_history += self.parse_dom(xml, searching_app_id, searching_date);   
                if key in ranking_history:
                    ranking_history[key] = ranking_history[key] + self.parse_dom(xml, searching_app_id, searching_date);
                else:                
                    ranking_history[key] = self.parse_dom(xml, searching_app_id, searching_date);
      
        for key in model.AppDef.urls.keys():       
            setattr(entry_rank_history,key,zlib.compress(ranking_history[key]));
#                entity.rankHistory = zlib.compress(ranking_history);
            
        entry_rank_history.put();
        print "RESULT*****"
        print ranking_history;
        print "</br>"
        
    def generate_from_source2(self,searching_app_id):
        global rankCode;

        today = datetime.date.today();
        print searching_app_id; 
        DURATION = 100;
        for i in range(0,DURATION):
            time.sleep(1);
            searching_date = today -  timedelta(i)
            print searching_date

            db_name = "SourceEntry";
            q = db.GqlQuery("SELECT * FROM " + db_name +" where date = DATE('" + str(searching_date) + "') ");

            results = q.fetch(1);
            if len(results) == 0:
                continue;

            entry = results[0];
            entry_rank_history = model.RankHistory();
            for key in model.AppDef.urls.keys():
                ranking_history = "";
                print key;
                compressed_xml = getattr(entry,key);
                if compressed_xml == None:
                    continue;
                xml = zlib.decompress(compressed_xml); 
#                print xml;
                ranking_history += self.parse_dom(xml, searching_app_id, searching_date);                 
                
                entry_rank_history.appId = int(searching_app_id) 
                setattr(entry_rank_history,key,zlib.compress(ranking_history));
#                entity.rankHistory = zlib.compress(ranking_history);
            
            entry_rank_history.put();
        print "RESULT*****"
        print ranking_history;
        print "</br>"
    
    def append(self,appId,rank):
        q = model.RankHistory.all();
        q.filter("appId", appId);
        results = q.fetch(1);
        
        entry = results[0]
        
        for k,v in rank.iteritems():
            rank_compressed = getattr(entry,k);
            rank_decompressed = zlib.decompress(rank_compressed);
            rank_decompressed = str(v) + rank_decompressed;
            rank_compressed = zlib.compress(rank_decompressed);
            setattr(entry,k,rank_compressed);
        entry.put();
        
    def get(self):
        mode = self.request.get("mode")
        if mode == "generate_from_source":
            searching_app_id = self.request.get("appId")
            self.generate_from_source(searching_app_id);
        elif mode == "append":
            searching_app_id = self.request.get("appId")
#            rank = self.request.get("rank");
            d = {"topFree":"a","topPaid":50};
            self.append(int(searching_app_id),d);
        elif mode == "get_ranking_history":
            searching_app_id = self.request.get("appId")
            self.get_ranking_history(searching_app_id)
                
application = webapp.WSGIApplication([('/.*', MainPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()  
    
    
