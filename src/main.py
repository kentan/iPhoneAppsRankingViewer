# -*- coding:utf-8 -*- 
'''
Created on 2013/02/11

@author: kentan
'''
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from xml.dom import minidom


import logging
import urllib2
import datetime
import model
import random
import zlib
from model import RankHistory
from datetime import timedelta;

class MainPage(webapp.RequestHandler):
    def get(self):
        mode = self.request.get("mode")
        if(mode == "crawl") :
            self.crawl();
            

        elif mode == "getAppList":
            self.getAppList();
            
    
    def putNewlyFoundTitleToDB(self,entity,title,url,iconUrl,date):

        q = entity.all();
        q.filter("title=",title);
        result = q.fetch(1);
        if(len(result) == 0):
            newlyFoundApp = model.NewlyFoundApp(title = title,date = date,url=url,iconUrl=iconUrl);
            newlyFoundApp.put();

    def getAppList(self):
        table = self.request.get("table")
        q = model.AppDef.dbModels.get(table).all();
        q.order("-date")
        q.filter("rank =", 0)

        results = q.fetch(30);
        htmlString = "";
        htmlString += '<ul data-role="listview" data-inset="true">'
        for entry in results:

            if entry.iconUrl == None or str(entry.iconUrl) == "http://localhost":
                continue;
            htmlString += '<li>'
            htmlString += '<a href="' + str(entry.url) + '" target="_blank">'
            htmlString += '<img src="' + str(entry.iconUrl) + '" />'
            htmlString +=  '<p><h3>' + str(entry.date) + '</h3></p>'
            htmlString +=  '<p>' + entry.title + '</p>'
            htmlString +=  '<p>' + entry.desc + '</p>'
            htmlString +=  '</a>'
            htmlString += '</li>'
        htmlString += '</ul>'

        self.response.out.write(htmlString);    

    def crawl(self):
        recodedDate = datetime.date.today();
        sourceEntry = model.SourceEntry(date = recodedDate);
        for key in model.AppDef.urls.keys():
            AppEntryInst = model.AppDef.dbModels.get(key);
            appEntryHistoryInst = model.AppDef.dbHistoryModels.get(key);
            url = model.AppDef.urls.get(key);
            try:
                response = urllib2.urlopen(url)
                xmlInString = response.read();
                dom = minidom.parseString(xmlInString)
                nodeFeed = dom.childNodes[0];
                rank = 0;
                title = "";
                url = "";
                iconUrl = "";
                imid = "";
                desc = "";

                model.AppDef.dbSourceModels.get(key)(model.AppDef(),sourceEntry,xmlInString);
  
                for n in nodeFeed.childNodes:
                    if rank >= 51:
                        break;
                    if isinstance(n,minidom.Element) and n.nodeName == "entry":
                        isTitleDone = False;
                        isDescDone = False;
                        isUrlDone = False;
                        isIconUrlDone = False;
                        for n2 in n.childNodes:
    
                            if isinstance(n2,minidom.Element):
                                if n2.nodeName == "title":
                                    #self.response.out.write(n2.firstChild.data);
                                    title = n2.firstChild.data;
                                    isTitleDone = True;

                                elif n2.nodeName == "im:image":
                                    iconUrl = n2.firstChild.data
                                    isIconUrlDone = True;
                                elif n2.nodeName == "id":
                                    url = n2.firstChild.data;
                                    imid = n2.attributes['im:id'].value;
                                    isUrlDone = True;
                                elif n2.nodeName == "summary":
                                    desc = n2.firstChild.data;                                  
                                    isDescDone = True;
                                # There is no summary element in new,newFree,newPaid xml.
                                # Because it's not necessary to show ranking history as for 
                                # new, newFree and newPaid feed, this if statement isn't invalid.
                                # However this code doesn't contain readability, adding if statement
                                # excluding new,newFree and newPaid is desirable.
                                elif isTitleDone and isUrlDone and isDescDone and isIconUrlDone:

                                    rank_coded = model.rankCode[rank];
                                    try:
                                        self.appendToRankHistory(imid, title,key,rank_coded,recodedDate);
                                    except Exception,e:
                                        logging.error("error in append");
                                        logging.error(e);
                                    break;

                        if(rank == 0):
                            # put rank0 to the history entities
                            appHistoryEntry = appEntryHistoryInst(title = title,date = recodedDate,url = url,iconUrl = iconUrl);
                            appHistoryEntry.put();
                            # if this title is newly found,then put this to newlyfound entity
                            self.putNewlyFoundTitleToDB(appEntryHistoryInst, title, url,iconUrl,recodedDate)
                            
                        appEntry = AppEntryInst(title = title,desc = desc,rank = rank,date = recodedDate,url=url,iconUrl=iconUrl,source = n);
                        appEntry.put();
                        rank += 1;    
                response.close();    

            except Exception,e:
                logging.error("error in main")
                logging.error(e);
                raise;
        sourceEntry.put();        
        
#    def appendToRankHistory(self,appId,appName,appType,rank,date_,m):
#        q = model.RankHistory.all();
#        q.filter("appId", int(appId));
#        results = q.fetch(1);
#        r = "";
#        if len(results) == 0:
#            entry = model.RankHistory();
#            entry.appId = int(appId);
#            entry.appName = appName;
#            rank_decompressed = str(rank);
#            if int(appId) == 595291824:
#                m.response.out.write("</br>RRRR1:" + str(rank) + ":"+ str(date_) + ":" +str(appType));
#        else:
#            entry = results[0]
#            rank_compressed = getattr(entry,appType);
#            if rank_compressed == None:
#                rank_decompressed = str(rank);
#                if int(appId) == 595291824:
#                    m.response.out.write("</br>RRRR2:" + str(rank) + ":"+ str(date_) + ":" +str(appType));
#            else:
#                lastUpdated = entry.lastUpdated;
#                d = date_ -   timedelta(1);
#                m.response.out.write("</br>:" + str(d) + ":"+ str(lastUpdated) + ":" +str(appType));
#                while(lastUpdated < d):
#                    r += "P"
#                    d -=  timedelta(1);
#                    if int(appId) == 595291824:
#                        m.response.out.write("</br>RRRR3:" + str(rank) + ":"+ str(date_) + ":" +str(appType));
#                
#                if int(appId) == 595291824:
#                    m.response.out.write("</br>RRRR4:" + str(rank) + ":"+ str(date_) + ":" +str(appType));                    
#                rank_decompressed = zlib.decompress(rank_compressed);
#                rank_decompressed = r  + str(rank) + rank_decompressed;
#
#                    
#                    
#        rank_compressed = zlib.compress(rank_decompressed);
#        setattr(entry,appType,rank_compressed);
#        entry.lastUpdated = date_;
#        entry.put();    
    def appendToRankHistory(self,appId,appName,appType,rank,date_):
        q = model.RankHistory.all();
        q.filter("appId", int(appId));
        q.filter("appType",appType);
        results = q.fetch(1);
        r = "";
        if len(results) == 0:
            entry = model.RankHistory();
            entry.appId = int(appId);
            entry.appName = appName;
            entry.appType = appType;
            rank_decompressed = str(rank);
        else:
            entry = results[0]
            rank_compressed = entry.rank;
            lastUpdated = entry.lastUpdated;
            d = date_ -   timedelta(1);

            while(lastUpdated < d):
                r += "P"
                d -=  timedelta(1);
            
            rank_decompressed = zlib.decompress(rank_compressed);
            rank_decompressed = str(rank) + r + rank_decompressed;

                    
                    
        rank_compressed = zlib.compress(rank_decompressed);
        entry.rank = rank_compressed
        entry.lastUpdated = date_;
        entry.put();    


application = webapp.WSGIApplication([('/.*', MainPage)], debug=True)
                
def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()