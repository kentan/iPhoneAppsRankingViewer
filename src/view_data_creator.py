# -*- coding:utf-8 -*- 
'''
Created on 2013/02/11

@author: kentan
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import model
import datetime
import zlib

class ViewDataCreator(webapp.RequestHandler):
    def get(self):
        mode = self.request.get("mode")
        if mode == "getAppList":
            table = self.request.get("table")
            q = model.AppDef.dbModels.get(table).all();
            q.order("-date")
            q.filter("rank =", 0)

            results = q.fetch(100);
            htmlString = "";
            htmlString += '<ul data-role="listview" data-inset="true">'
            for entry in results:

                if entry.iconUrl == None or str(entry.iconUrl) == "http://localhost":
                    continue;
                htmlString += '<li>'
                htmlString += '<a href="#page_details" date="' + str(entry.date) +'" class="list_element">';
                htmlString += '<img src="' + str(entry.iconUrl) + '" />'
                htmlString +=  '<p><h3>' + str(entry.date) + '</h3></p>'
                htmlString +=  '<p>' + entry.title + '</p>'
                htmlString +=  '<p>' + entry.desc + '</p>'
                htmlString +=  '</a>'
                htmlString += '</li>'
            htmlString += '</ul>'

            self.response.out.write(htmlString);    
        elif mode == "getAppDetails":
            table = self.request.get("table")
            dbName = model.AppDef.dbModels.get(table).name;
            date_ = self.request.get("date")

#            q.filter("date =", "DATE('" + date_ + "')");
#            q.order("rank");

            q = db.GqlQuery("SELECT * FROM " + dbName +" where date = DATE('" + date_ + "') order by rank");

            results = q.fetch(100);
            htmlString = "";
            htmlString += '<ul data-role="listview" data-inset="true">'

            for entry in results:

                if entry.iconUrl == None or str(entry.iconUrl) == "http://localhost":
                    continue;
                htmlString += '<li>'
                htmlString += '<a href="#page_chart" rank="' + str(entry.rank + 1) + '" class=list_element_details>'
#                htmlString += '<a href="#page_chart?rank=' + str(entry.rank + 1) + '" target="_blank">'
#                htmlString += '<a href="chart.html?appName=' + entry.title + '&rank=' + str(entry.rank + 1) + '" target="_blank">'
                htmlString += '<img src="' + str(entry.iconUrl) + '" />'
                htmlString +=  '<p><h3 class="title" url="' + entry.url + '" rank="' + str(entry.rank) + '">' + str(entry.rank + 1) +' . '+ entry.title +'</h3></p>'
                htmlString +=  '<p class="desc">' + entry.desc + '</p>'
                htmlString +=  '</a>'
                htmlString += '</li>'
            htmlString += '</ul>'

            self.response.out.write(htmlString);  
        elif mode == "getChartData":
            self.getChartData();
                        
    def getChartData(self):
        searching_app_name = self.request.get("appName")
        q = model.RankHistory.all();
#        q.filter("appId", int(searching_app_name));

        q.filter("appName", searching_app_name);
        results = q.fetch(1);
        
        if len(results) == 0:
            return "{}";
        
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


application = webapp.WSGIApplication([('/.*', ViewDataCreator)], debug=True)
                
def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()