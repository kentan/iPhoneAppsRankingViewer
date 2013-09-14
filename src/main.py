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

class MainPage(webapp.RequestHandler):
    def get(self):
        mode = self.request.get("mode")
        if(mode == "crawl") :
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
#                    sourceEntry.topFree = xmlInString;
                    model.AppDef.dbSourceModels.get(key)(model.AppDef(),sourceEntry,xmlInString);
                    
                    for n in nodeFeed.childNodes:
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
#                                        iconGetter = icon_getter.IconGetter();
#                                        iconUrl = iconGetter.getIcon(url);
#                                        iconUrl = "http://localhost";#TODO
                                        imid = n2.attributes['im:id'].value;
                                        rank_coded = model.rankCode[rank];
                                        
                                        self.appendToRankHistory(imid, key, rank_coded);
                                        
                                        isUrlDone = True;
                                    elif n2.nodeName == "summary":
                                        desc = n2.firstChild.data;                                  
                                        isDescDone = True;
                                        
                                    elif isTitleDone and isUrlDone and isDescDone and isIconUrlDone:
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
            sourceEntry.put();
            

        elif mode == "getAppList":
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

            
#        elif mode == "putDummyData":
#            dbName = self.request.get("db")
#            entity = model.AppDef.dbModels.get(dbName);
#            self.putDummyDataToDB(entity);
#        elif mode =="get":
#            q = model.AppEntry.all();
#            results = q.fetch(1000);
#            for entry in results:
#                self.response.out.write(entry.title + "</br>");

#        elif mode == "delete":
#            for inst in model.AppDef.dbModels.values():
#                q = inst.all(keys_only=True)
#                results = q.fetch(10000)
#                db.delete(results);
#                    self.response.out.write("deleted")
#                self.response.out.write("delete comment-outed line for delete !!")
    
    def putNewlyFoundTitleToDB(self,entity,title,url,iconUrl,date):

        q = entity.all();
        q.filter("title=",title);
        result = q.fetch(1);
        if(len(result) == 0):
            newlyFoundApp = model.NewlyFoundApp(title = title,date = date,url=url,iconUrl=iconUrl);
            newlyFoundApp.put();

    def appendToRankHistory(self,appId,appType,rank):
        q = model.RankHistory.all();
        q.filter("appId", appId);
        results = q.fetch(1);
        
        entry = results[0]
        if len(results) == 0:
            entry = model.RankHistory();
            entry.appId = int(appId);
            rank_decompressed = str(rank);
        else:
            rank_compressed = getattr(entry,appType);
            rank_decompressed = zlib.decompress(rank_compressed);
            rank_decompressed = str(rank) + rank_decompressed;
        rank_compressed = zlib.compress(rank_decompressed);
        setattr(entry,appType,rank_compressed);
        entry.date = datetime.date.today();
        entry.put();    
#    def putDummyDataToDB(self,entity):
#
##            for index in range(0,100):
##                dummyString = "dummy" + str(index);
##
##                dummyRank = random.randint(0,10);
##                dummyDate = datetime.date(2013, 3, random.randint(1,31))
##                q = entity(title=dummyString,rank=dummyRank,desc=dummyString,date=dummyDate,url="http://google.com",iconUrl="http://a2.mzstatic.com/us/r1000/077/Purple/v4/c2/4f/29/c24f29f4-8d24-b345-7609-085e15a06805/mzl.junlfvwk.png");
##                q.put();  
#            
#            url = "https://itunes.apple.com/jp/rss/topfreeapplications/limit=10/xml";
#            response = urllib2.urlopen(url)
#            xmlInString = response.read();
#            sourceEntry = model.SourceEntry(date=datetime.date.today())
#            key = "topFree";
#            model.AppDef.dbSourceModels.get(key)(model.AppDef(),sourceEntry,xmlInString);
#            response.close();
#            sourceEntry.put();
                                  
        

application = webapp.WSGIApplication([('/.*', MainPage)], debug=True)
                
def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()