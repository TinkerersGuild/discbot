from plugins import PluginResponse, Plugin
import sys
import requests
import html2text
from bs4 import BeautifulSoup

MAXLINES = 12



class lyrics(Plugin):    
        myhelp = """Usage: !lyrics <songname>. Goes and looks up the AZLyrics db for lyrics to the song """

        def __init__(self, dbconn):
                self.keyword = ("lyrics",)
                self.response = PluginResponse()
        def build_url(self, searchstr):
            return ("https://search.azlyrics.com/search.php?q={}".format(searchstr))

        def command(self, args):
                text = args.text
                

                try:
                    if (text != ' '):
                        searchstr = "+".join(text.split())              
                        print(searchstr)
                        url = self.build_url(searchstr)
                        print(url)
                        resp = requests.get(url)
                        print(resp)
                        if (resp.status_code == 200):
                            txtcount = 0    
                            txt = ""
                            soup = BeautifulSoup(resp.text, 'html.parser')    
                            link = soup.find_all('td', class_="text-left visitedlyr")[0]
                            print("Link:{}".format(link))
                            url =  link.find_all('a')[0].get("href")
                            print("URL:{}".format(url))
                            resp = requests.get(url)
                            print("Resp:{}".format(resp))
                            print("=================================")
                            if (resp.status_code == 200):
                                    soup = BeautifulSoup(resp.text, 'html.parser')    
                                    #print("Response: {}".format(resp.text))
                                    txt = soup.find_all('div', class_="")[0].contents
                                    print("Lyrics: {}".format(txt))
                                    ftxt = ''    
                                    for ln in txt[2:]:    
                                        try:
                                                ftxt += html2text.html2text(ln).strip()+"\n"
                                        except:
                                                ftxt += "" 

                                        #if (txtcount < MAXLINES):
                                                #txt += "{}".format(link)
                                                #txtcount += 1
                                        #else:
                                                #txt += "More: {}".format(url)                       
                                                #txtcount += 1
                                                #break
                                    print(ftxt)
                                    self.response.setText(ftxt)
                        else:
                            self.response.setText("Not found")


                    else:
                        self.response.setText(myhelp)
                except: 
                        e = sys.exc_info()[0]
                        print("nope {}".format(e))
                        self.response.setText( "NFI {}".format(e))
                return self.response

