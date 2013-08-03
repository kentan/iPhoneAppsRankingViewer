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
                htmlString += '<a href="' + str(entry.url) + '" target="_blank">'
                htmlString += '<img src="' + str(entry.iconUrl) + '" />'
                htmlString +=  '<p><h3>' + str(entry.rank + 1) +' . '+ entry.title +'</h3></p>'
#                htmlString +=  '<p>' + entry.title + '</p>'
                htmlString +=  '<p>' + entry.desc + '</p>'
                htmlString +=  '</a>'
                htmlString += '</li>'
            htmlString += '</ul>'

            self.response.out.write(htmlString);  

application = webapp.WSGIApplication([('/.*', ViewDataCreator)], debug=True)
                
def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()