# -*- coding:utf-8 -*- 
from google.appengine.ext import db
import zlib;
class SourceEntry(db.Model):
    topFree = db.BlobProperty();    
    topPaid = db.BlobProperty();
    topGrossing = db.BlobProperty();
    topFreeIpad = db.BlobProperty();
    topPaidIpad = db.BlobProperty();
    topGrossingIpad = db.BlobProperty();
    new = db.BlobProperty();
    newFree = db.BlobProperty();    
    newPaid = db.BlobProperty();
    date = db.DateProperty();
    
class AppEntry(db.Model):
    title = db.StringProperty(required=True)
    desc = db.TextProperty(required=True)
    rank = db.IntegerProperty(required=True);
    url = db.URLProperty();
    iconUrl = db.URLProperty();
    date = db.DateProperty();

class AppEntryTopFree(AppEntry):
    dummy = "";
class AppEntryTopPaid(AppEntry):
    dummy = "";
class AppEntryTopGrossing(AppEntry):#top sales
    dummy = "";
class AppEntryTopFreeIpad(AppEntry):
    dummy = "";  
class AppEntryTopPaidIpad(AppEntry):
    dummy = "";   
class AppEntryTopGrossingIpad(AppEntry):
    dummy = "";    
class AppEntryNew(AppEntry):
    dummy = "";
class AppEntryNewFree(AppEntry):
    dummy = "";
class AppEntryNewPaid(AppEntry):
    dummy = "";
    
class AppEntryTop20Holder(db.Model):
    title = db.StringProperty();
    date = db.DateProperty();
    
class AppEntryTopFree20Holder(AppEntryTop20Holder):
    dummy = "";
class AppEntryTopPaid20Holder(AppEntryTop20Holder):
    dummy = "";    

class NewlyFoundApp(db.Model):
    title = db.StringProperty();
    date = db.DateProperty();


class AppDef:
    topFree = "topFree";
    topPaid = "topPaid";
    topGrossing = "topGrossing";
    topFreeIpad = "topFreeIpad";
    topPaidIpad = "topPaidIpad";
    topGrossingIpad = "topGrossingIpad";
    new = "new";
    newFree = "newFree";
    newPaid = "newPaid";
    num = 50;
#    urls = {topFree:"https://itunes.apple.com/jp/rss/topfreeapplications/limit=" + str(num) + "/xml",
#     }        

    urls = {topFree:"https://itunes.apple.com/jp/rss/topfreeapplications/limit=" + str(num) + "/xml",
     topPaid:"https://itunes.apple.com/jp/rss/toppaidapplications/limit=" + str(num) + "/xml",
     topGrossing:"https://itunes.apple.com/jp/rss/topgrossingapplications/limit=" + str(num) + "/xml",
     topFreeIpad:"https://itunes.apple.com/jp/rss/topfreeipadapplications/limit=" + str(num) + "/xml",
     topPaidIpad:"https://itunes.apple.com/jp/rss/toppaidipadapplications/limit=" + str(num) + "/xml",
     topGrossingIpad:"https://itunes.apple.com/jp/rss/topgrossingipadapplications/limit=" + str(num) + "/xml",
     new:"https://itunes.apple.com/jp/rss/newapplications/limit=" + str(num) + "/xml",
     newFree:"https://itunes.apple.com/jp/rss/newfreeapplications/limit=" + str(num) + "/xml",
     newPaid:"https://itunes.apple.com/jp/rss/newpaidapplications/limit=" + str(num) + "/xml"
     }        
    def setSourceToTopFree(self,e,source):
        e.topFree = zlib.compress(source);
    def setSourceToTopPaid(self,e,source):
        e.topPaid = zlib.compress(source);
    def setSourceToTopGrossing(self,e,source):
        e.topGrossing = zlib.compress(source);        
    def setSourceToTopFreeIpad(self,e,source):
        e.topFreeIpad = zlib.compress(source);
    def setSourceToTopPaidIpad(self,e,source):
        e.topPaidIpad = zlib.compress(source);
    def setSourceToTopGrossingIpad(self,e,source):
        e.topGrossingIpad = zlib.compress(source);
    def setSourceToNew(self,e,source):
        e.new = zlib.compress(source);
    def setSourceToNewFree(self,e,source):
        e.newFree = zlib.compress(source);
    def setSourceToNewPaid(self,e,source):
        e.newPaid = zlib.compress(source);    
        
    dbModels = {topFree:AppEntryTopFree,
     topPaid:AppEntryTopPaid,
     topGrossing:AppEntryTopGrossing,
     topFreeIpad:AppEntryTopFreeIpad,
     topPaidIpad:AppEntryTopPaidIpad,
     topGrossingIpad:AppEntryTopGrossingIpad,
     new:AppEntryNew,
     newFree:AppEntryNewFree,
     newPaid:AppEntryNewPaid
     }
    
    dbHistoryModels = {topFree:AppEntryTopFree20Holder,
     topPaid:AppEntryTopPaid20Holder,
     topGrossing:AppEntryTop20Holder,#TBD
     topFreeIpad:AppEntryTop20Holder,#TBD
     topPaidIpad:AppEntryTop20Holder,#TBD
     topGrossingIpad:AppEntryTop20Holder,#TBD
     new:AppEntryTop20Holder,#TBD
     newFree:AppEntryTop20Holder,#TBD
     newPaid:AppEntryTop20Holder#TBD
     }
    dbSourceModels = {topFree:setSourceToTopFree,
     topPaid:setSourceToTopPaid,
     topGrossing:setSourceToTopGrossing,
     topFreeIpad:setSourceToTopFreeIpad,
     topPaidIpad:setSourceToTopPaidIpad,
     topGrossingIpad:setSourceToTopGrossingIpad,
     new:setSourceToNew,
     newFree:setSourceToNewFree,
     newPaid:setSourceToNewPaid
     }