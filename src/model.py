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
    desc = db.TextProperty()
    rank = db.IntegerProperty(required=True);
    url = db.URLProperty();
    iconUrl = db.URLProperty();
    date = db.DateProperty();

class AppEntryTopFree(AppEntry):
    name = "AppEntryTopFree";
class AppEntryTopPaid(AppEntry):
    name = "AppEntryTopPaid"
class AppEntryTopGrossing(AppEntry):#top sales
    name = "AppEntryTopGrossing";
class AppEntryTopFreeIpad(AppEntry):
    name = "AppEntryTopFreeIpad";
class AppEntryTopPaidIpad(AppEntry):
    name = "AppEntryTopPaidIpad";
class AppEntryTopGrossingIpad(AppEntry):
    name = "AppEntryTopGrossingIpad";
class AppEntryNew(AppEntry):
    name= "AppEntryNew";
class AppEntryNewFree(AppEntry):
    name = "AppEntryNewFree";
class AppEntryNewPaid(AppEntry):
    name = "AppEntryNewPaid";
    
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

class RankHistory(db.Model):
    appId = db.IntegerProperty();
    appName = db.StringProperty();
    appType = db.StringProperty();
    rank = db.BlobProperty();
    lastUpdated = db.DateProperty();
#class RankHistory(db.Model):
#    appId = db.IntegerProperty();
#    appName = db.StringProperty();
#    topFree = db.BlobProperty();
#    topPaid = db.BlobProperty();
#    topGrossing = db.BlobProperty();
#    topFreeIpad = db.BlobProperty();
#    topPaidIpad = db.BlobProperty();
#    topGrossingIpad = db.BlobProperty();
#    new = db.BlobProperty();
#    newFree = db.BlobProperty();    
#    newPaid = db.BlobProperty();
#    lastUpdated = db.DateProperty();
        
rankCode = {0:"0",
            1:"1",
            2:"2",
            3:"3",
            4:"4",
            5:"5",
            6:"6",
            7:"7",
            8:"8",
            9:"9",
            10:"a",
            11:"b",
            12:"c",
            13:"d",
            14:"e",
            15:"f",
            16:"g",
            17:"h",
            18:"i",
            19:"j",
            20:"k",
            21:"l",
            22:"m",
            23:"n",
            24:"o",
            25:"p",
            26:"q",
            27:"r",
            28:"s",
            29:"t",
            30:"u",
            31:"v",
            32:"w",
            33:"x",
            34:"y",
            35:"z",
            36:"A",
            37:"B",
            38:"C",
            39:"D",
            40:"E",
            41:"F",
            42:"G",
            43:"H",
            44:"I",
            45:"J",
            46:"K",
            47:"L",
            48:"M",
            49:"N",
            50:"O",
            51:"P",
            52:"Q",
            53:"R",
            54:"S",
            55:"T",
            56:"U",
            57:"V",
            58:"W",
            59:"X",
            60:"Y",
            61:"Z",
            }
rankDecode = {"0":0,
            "1":1,
            "2":2,
            "3":3,
            "4":4,
            "5":5,
            "6":6,
            "7":7,
            "8":8,
            "9":9,
            "a":10,
            "b":11,
            "c":12,
            "d":13,
            "e":14,
            "f":15,
            "g":16,
            "h":17,
            "i":18,
            "j":19,
            "k":20,
            "l":21,
            "m":22,
            "n":23,
            "o":24,
            "p":25,
            "q":26,
            "r":27,
            "s":28,
            "t":29,
            "u":30,
            "v":31,
            "w":32,
            "x":33,
            "y":34,
            "z":35,
            "A":36,
            "B":37,
            "C":38,
            "D":39,
            "E":40,
            "F":41,
            "G":42,
            "H":43,
            "I":44,
            "J":45,
            "K":46,
            "L":47,
            "M":48,
            "N":49,
            "O":50,
            "P":51,
            "Q":52,
            "R":53,
            "S":54,
            "T":55,
            "U":56,
            "V":57,
            "W":58,
            "X":59,
            "Y":60,
            "Z":61,
            }  