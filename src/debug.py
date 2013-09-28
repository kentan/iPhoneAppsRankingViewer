
import model;
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from xml.dom import minidom
import urllib2
import datetime
import random
import zlib
from datetime import timedelta;
import time;
import re;
import main;

class MainPage(webapp.RequestHandler):
    def deleteAll(self):
        for inst in model.AppDef.dbModels.values():
            q = inst.all(keys_only=True)
            results = q.fetch(10000)
            db.delete(results);
            self.response.out.write("deleted")
            self.response.out.write("delete comment-outed line for delete !!")
        q = model.RankHistory.all();
        results = q.fetch(10000)
        db.delete(results);
        
        q = model.SourceEntry.all();
        results = q.fetch(10000)
        db.delete(results);

        q = model.NewlyFoundApp.all();
        results = q.fetch(10000)
        db.delete(results);        
        
        q = model.AppEntryNew.all();
        results = q.fetch(10000)
        db.delete(results);        

        q = model.AppEntryTop20Holder.all();
        results = q.fetch(10000)
        db.delete(results);                
        
        q = model.AppEntryTopFree20Holder.all();
        results = q.fetch(10000)
        db.delete(results);                

        q = model.AppEntryTopPaid20Holder.all();
        results = q.fetch(10000)
        db.delete(results);                

    
    
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
    
#    def get(self):
#        entity = model.AppDef.dbModels.get("topFree");
#        self.putDummyDataToDB(entity);
#    def appendToRankHistory(self,appId,appName,appType,rank,searchingDate):
#        q = model.RankHistory.all();
#        q.filter("appId", int(appId));
#        results = q.fetch(1);
#        r = "";
#        if len(results) == 0:
#            entry = model.RankHistory();
#            entry.appId = int(appId);
#            entry.appName = appName;
#            rank_decompressed = model.rankCode[rank];
#        else:
#            entry = results[0]
#            rank_compressed = getattr(entry,appType);
#            if rank_compressed == None:
#                rank_decompressed = model.rankCode[rank];
#            else:
#                lastUpdated = entry.lastUpdated;
#                d = searchingDate-   timedelta(1);
#                while(lastUpdated < d):
#                    r += "P"
#                    d -=  timedelta(1);
#
#                    
#                rank_decompressed = zlib.decompress(rank_compressed);
#                rank_decompressed = r  + model.rankCode[rank] + rank_decompressed;
#
#                    
#                    
#        rank_compressed = zlib.compress(rank_decompressed);
#        setattr(entry,appType,rank_compressed);
#        entry.lastUpdated = searchingDate;
#        entry.put();
    
    def crawlFromXml(self,xml,searching_date,searching_key):
#       self.response.out.write(xml);
        recodedDate = searching_date;

        m = main.MainPage();
        for key in model.AppDef.urls.keys():
            if searching_key != key:
                continue;
            
            AppEntryInst = model.AppDef.dbModels.get(key);
            appEntryHistoryInst = model.AppDef.dbHistoryModels.get(key);

            try:

                xmlInString = xml;
                dom = minidom.parseString(xmlInString)
                nodeFeed = dom.childNodes[0];
                rank = 0;
                title = "";
                url = "";
                iconUrl = "";
                imid = "";
                _desc = "";
#                    sourceEntry.topFree = xmlInString;
  
                for n in nodeFeed.childNodes:
#                        print str(rank)
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
                                    _desc = n2.firstChild.data;   
                                    isDescDone = True;
                                    
                                elif isTitleDone and isUrlDone and isDescDone and isIconUrlDone:

                                    rank_coded = model.rankCode[rank];
                                    try:
                                        m.appendToRankHistory(imid, title,key,rank_coded,recodedDate);
                                    except Exception,e:
                                        raise;
                                    break;


#                        if(rank == 0):
#                            # put rank0 to the history entities
#                            appHistoryEntry = appEntryHistoryInst(title = title,date = recodedDate,url = url,iconUrl = iconUrl);
#                            appHistoryEntry.put();
#                            # if this title is newly found,then put this to newlyfound entity
#                            m.putNewlyFoundTitleToDB(appEntryHistoryInst, title, url,iconUrl,recodedDate)
                            
#                        appEntry = AppEntryInst(title = title,desc = _desc,rank = rank,date = recodedDate,url=url,iconUrl=iconUrl,source = n);
#                        appEntry.put();
                        rank += 1;    


            except Exception,e:
                self.response.out.write(e);
                raise;

    def restoreDataFromSourceEntry(self):
        today = datetime.date.today();

        DURATION = 20;

        for i in range(0,DURATION):
            searching_date = today -  timedelta(DURATION - i)
            self.response.out.write( searching_date);

            q = db.GqlQuery("SELECT * FROM SourceEntry where date = DATE('" + str(searching_date) + "') ");
            results = q.fetch(1);
            if len(results) == 0:
                self.response.out.write("no data</br>");
                continue;
            entry = results[0];
            for key in model.AppDef.urls.keys():
                compressed_xml = getattr(entry,key);
                decompressed_xml = zlib.decompress(compressed_xml).strip()
                self.crawlFromXml(decompressed_xml,searching_date,key);
#                self.response.out.write(decompressed_xml);
                
    
    def putSouceFromCloud(self,appType):
        
        DURATION = 10;


        for diff in range(1,DURATION):
#            url = "http://localhost:8080/debug.py?mode=get&appType=" + appType + "&diff=" + str(diff);
            url = "http://simdott02.appspot.com/debug.py?mode=getSourceFromCloud&appType=" + appType + "&diff=" + str(diff);
            response = urllib2.urlopen(url)
            rowData = response.read();
            response.close();
#            self.response.out.write("</br>******</br>" + rowData);
#            return;
#            rowData2 = re.split("Content-Length:",rowData)[1];
            rowData2 = "";
            try:
                rowData2 = re.split(r"Content-Length: [0-9]+",rowData)[1];
            except:
                continue;
            recodedDate = datetime.date.today() -  timedelta(int(diff))
            for key in model.AppDef.urls.keys():
                if appType == key:
                    q = db.GqlQuery("SELECT * FROM  SourceEntry where date = DATE('" + str(recodedDate) + "') ");
                    results = q.fetch(1);
                    sourceEntry = None;
                    if len(results) == 0:
                        sourceEntry = model.SourceEntry(date = recodedDate);
                    else:
                        sourceEntry = results[0]
                    model.AppDef.dbSourceModels.get(key)(model.AppDef(),sourceEntry,rowData2);
                    self.response.out.write("d");
                    sourceEntry.put();
                    break;
                
    def getSourceFromCloud(self,appType):
        today = datetime.date.today();

        diff =  self.request.get("diff")

        rv = "";

        searching_date = today -  timedelta(int(diff))
        print searching_date

        db_name = "SourceEntry";
        q = db.GqlQuery("SELECT * FROM " + db_name +" where date = DATE('" + str(searching_date) + "') ");

        results = q.fetch(1);
        if len(results) == 0:
            return;

        entry = results[0];
        for key in model.AppDef.urls.keys():
            if appType == key:
                compressed_xml = getattr(entry,key);
                self.response.out.write(zlib.decompress(compressed_xml));
                return ;
        
        
    def get(self):
        mode = self.request.get("mode")
#
        if mode == "putSouceFromCloud":
            for key in model.AppDef.urls.keys():
                pass;
#                self.putSouceFromCloud(key);
        elif mode == "getSourceFromCloud":
            appType =  self.request.get("appType")
            self.getSourceEntryFromColud(appType);
        elif mode == "deleteAll":
            pass;
#            self.deleteAll();
        elif mode == "restore":
            self.restoreDataFromSourceEntry();
            
application = webapp.WSGIApplication([('/.*', MainPage)], debug=True)
run_wsgi_app(application)
