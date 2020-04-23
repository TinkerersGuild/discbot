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

class jargon(Plugin):
    myhelp = """Usage: !jargon <term>. Goes and looks up the internet Jargon File for a definition of <term>"""
    def __init__(self, dbconn):
        self.keyword = ("jargon",)
        self.response = PluginResponse()
        self.jargonindex = list()
        self.jargonlower = dict()
        with open(storefile) as f:
            for line in f:
                j_entry = line.rstrip()
                if not (j_entry == '' ):
                    self.jargonindex.append(j_entry)
                    for i in j_entry.split():
                        if i.lower() in self.jargonlower:
                            self.jargonlower[i.lower()].append(j_entry)
                        else:
                            self.jargonlower[i.lower()] = [j_entry,]
        self.jarlength = len(self.jargonindex)

    def build_url(self, searchstr):
        searchstr = "-".join(searchstr.split())
        cap = searchstr[0]
        return "http://www.catb.org/jargon/html/{}/{}.html".format(cap.upper(), searchstr)

    def build_alt_list(self, searchstr):
        results = list()
        for mystr in searchstr.split():
            resp = self.jargonlower.get(mystr.lower(), "")
            if resp != "":
                for alt in resp:
                    results.append(self.build_url(alt))
        return results





    def command(self, args):
        text = args.text
        self.response.setText("Nope")
        searchstr = self.jargonindex[ random.randint(0,self.jarlength)] 


        if (text != ''):
            searchstr = text

        url = self.build_url(searchstr)
        resp = requests.get(url)
        if (resp.status_code == 200):
            txt = html2text.html2text(resp.text).split("\n")
            ftxt = ''

            txt = txt[6:-6]
            if (len(txt) > MAXLINES):
                txt = txt[:MAXLINES]

                txt[-1] += "\n(more ...)\n "

            for i in (txt):
                if (i.strip() != ''):
                    ftxt += i.strip() + "\n"

            ftxt += ("\n" + url)
            self.response.setText(ftxt)

        elif (resp.status_code == 404) :
            alt_list = self.build_alt_list(text)
            resp = " No entry for {0} ".format(url)
            if len(alt_list) > 0:
                for alt in alt_list:
                    resp += "\n Did you mean {} ?".format(alt)
                    
                    
            self.response.setText(resp)


        else:

            self.response.setText("I couldn't find that url! {0} ({1}) ".format(url, resp.status_code))
        return self.response
