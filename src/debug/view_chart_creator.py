# -*- coding:utf-8 -*- 
'''
Created on 2013/09/04

@author: kentan
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


import model
import zlib


class ViewChartCreator(webapp.RequestHandler):

    def get(self):
        searching_app_name = self.request.get("appName")
        q = model.RankHistory.all();
        q.filter("appId", int(searching_app_name));
        results = q.fetch(1);
        
        if len(results) == 0:
            return "";
        
        entry = results[0];
        
        rv = '{';
        for key in model.AppDef.urls.keys():
            compressed = getattr(entry,key);
            if compressed == None:
                continue;
            data = zlib.decompress(compressed);
 
            rv += ('"' + key + '":"' + data + '",');
        rv = rv[0:len(rv) - 1];
        rv += "}"
        self.response.out.write(rv); 
        
        

application = webapp.WSGIApplication([('/.*', ViewChartCreator)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()  
    
    
