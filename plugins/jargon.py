########
# Fetches jargon file entries
######
from plugins import PluginResponse, Plugin
import sys
import requests
import html2text
import random

storefile = "go01.html"

MAXLINES = 12
HELP = """Usage: !jargon <term>. Goes and looks up the internet Jargon File for a definition of <term>"""

class jargon(Plugin):
        def __init__(self, dbconn):
                self.keyword = ("jargon",)
                self.response = PluginResponse()
                self.jargonindex = list()
                with open(storefile) as f:
                    for line in f:
                        if not (line.rstrip() == '' ):
                            self.jargonindex.append(line.rstrip())
                #print(self.jargonindex)    
                self.jarlength = len(self.jargonindex)

        def command(self, args):
          text = args.text
          print(text)
          self.response.setText("Nope")
          searchstr = self.jargonindex[ random.randint(0,self.jarlength)] 


          if (text != ''):
                  searchstr = text
                  print("Gotcha!" + searchstr)
                
          searchstr = "-".join(searchstr.split())
          cap = searchstr[0].upper()
          url = "http://www.catb.org/jargon/html/{}/{}.html".format(cap, searchstr)
          #print(url)
          resp = requests.get(url)
          if (resp.status_code == 200):
          #print(resp)
                  txt = html2text.html2text(resp.text).split("\n")
                  ftxt = ''

                  txt = txt[6:-6]
                  if (len(txt) > MAXLINES):
                          txt = txt[:MAXLINES]
                        
                          txt[-1] += "\n(more ...)\n "
                
                  for i in (txt):
                          print(".{}.".format(i))
                          if (i.strip() != ''):
                                  ftxt += i.strip() + "\n"
                                

                  ftxt += ("\n" + url)
                  self.response.setText(ftxt)
                                
          else:

                  self.response.setText("I couldn't find that url! {} ".format(url))
          return self.response
