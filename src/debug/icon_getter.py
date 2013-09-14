# -*- coding:utf-8 -*- 
'''
Created on 2013/02/11

@author: kentan
'''

import HTMLParser
import urllib2
import logging
import model

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(30)
# create a subclass and override the handler methods
class AppWebHtmlParser(HTMLParser.HTMLParser):
    iconUrl = "";

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            if attrs[0][0] == "content" and attrs[1][0] == "property" and attrs[1][1] == "og:image" :
                self.iconUrl = attrs[0][1];


class IconGetter:
    userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.152 Safari/537.22"
    hdr = {'User-Agent': 'iTunes/10.4.1 (Macintosh; Intel Mac OS X 10.6.8) AppleWebKit/534.50',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    def getIcon(self,url):
        try:
            req = urllib2.Request(url, headers=self.hdr) 
            response = urllib2.urlopen(req)
            content = response.read();
            parser = AppWebHtmlParser();
            parser.feed(content);
            response.close();
            return parser.iconUrl;
        except Exception,e:                    
            logging.error("error in getIcon")
            logging.error(url)
            logging.error(e);

class MainPage(webapp.RequestHandler):
    def get(self):
        
        ig = IconGetter();
        logging.debug("in get");
        for key in model.AppDef.dbModels:
            appEntry = model.AppDef.dbModels.get(key);
#            appEntryHistory = model.AppDef.dbHistoryModels.get(key);
            logging.debug("key " + key + " :in get");            
            q = appEntry.all();
            q.filter("rank =", 0)
            q.order("-date")
            results = q.fetch(10);
            for item in results:
                logging.debug("has result:in get");
                #TODO change not to insert iconUrl at initial put
#                if(str(item.iconUrl) == ""):
                logging.debug("has localhost url:in get");
                iconUrl = ig.getIcon(item.url);
                logging.debug("update to " +  str(iconUrl) + " :in get");
                if(str(iconUrl) == ""):
                    logging.debug("skip :in get");
                    continue;
                item.iconUrl= iconUrl;
                item.put();

#                    self.response.out.write(item.iconUrl);
#                    self.response.out.write("</br>");   
                     
application = webapp.WSGIApplication([('/.*', MainPage)], debug=True)
                
def main():
    run_wsgi_app(application)