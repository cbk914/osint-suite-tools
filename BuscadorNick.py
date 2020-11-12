'''
Copyright (c) 2020, QuantiKa14 Servicios Integrales S.L
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
'''

#AUTHOR: JORGE WEBSEC
#Twitter: @JorgeWebsec
#WEB: www.quantika14.com

import requests
from bs4 import BeautifulSoup
from validate_email import validate_email
from datetime import datetime
from datetime import timedelta
from html_reports.reports import Report
from search_engines import Google
from tldextract import extract

import modules.er as er
import modules.config as config
import modules.facebook as facebook

#REPORT INSTANCE
rep = Report()

emails = ("@gmail.com", "@yahoo.com", "@hotmail.com", "@hotmail.es", "@outlook.com", "@live.com", "@hushmail.com", "@me.com", "@mail.com", "@protonmail.com", "@facebook.com")

urls={"Facebook":"https://www.facebook.com/data",
      "YouTube":"https://www.youtube.com/user/data",
      "Codecanton":"https://codecanyon.net/user/",
      "Twitter":"https://twitter.com/data",
      "Instagram":"https://www.instagram.com/data/",
      "Blogger":"http://data.blogspot.com/",
      "GooglePlus":"http://plus.google.com/+data/",
      "Twitch":"https://www.twitch.tv/data",
      "Reddit":"http://www.reddit.com/user/data/",
      "WordPress":"https://data.wordpress.com/",
      "Ebay":"https://www.ebay.com/usr/data",
      "Pinterest":"https://www.pinterest.com/data/",
      "Yelp":"http://data.yelp.com",
      "Slack":"https://data.slack.com/",
      "GitHub":"https://github.com/data",
      "Tumblr":"https://data.tumblr.com/",
      "Flickr":"https://www.flickr.com/photos/data/",
      "ProductHunt":"https://www.producthunt.com/@data",
      "Steam":"https://steamcommunity.com/id/data",
      "Foursquare":"https://foursquare.com/data",
      "Vimeo":"https://vimeo.com/data",
      "Etsy":"https://www.etsy.com/people/data",
      "SoundCloud":"https://soundcloud.com/data",
      "BitBucket":"https://bitbucket.org/data/",
      "CashMe":"https://cash.me/$data/",
      "DailyMotion":"https://www.dailymotion.com/data",
      "Aboutme":"https://about.me/data",
      "Disqus":"https://disqus.com/by/data/",
      "Medium":"https://medium.com/@data/",
      "Behance":"https://www.behance.net/data",
      "Bitly":"https://bitly.com/u/data",
      "CafeMom":"http://cafemom.com/home/data",
      "Fanpop":"http://www.fanpop.com/fans/data",
      "deviantART":"https://data.deviantart.com/",
      "GoodReads":"https://www.goodreads.com/data",
      "Instructables":"http://www.instructables.com/member/data/",
      "Keybase":"https://keybase.io/data/",
      "Kongregate":"http://www.kongregate.com/accounts/data",
      "LiveJournal":"https://data.livejournal.com/",
      "AngelList":"https://angel.co/data",
      "LastFM":"https://www.last.fm/user/data",
      "Slideshare":"https://www.slideshare.net/data",
      "Tripit":"https://www.tripit.com/people/data#/profile/basic-info",
      "Fotolog":"https://fotolog.com/data/",
      "Dribbble":"https://dribbble.com/data",
      "Imgur":"https://imgur.com/user/data",
      "Tracky":"https://tracky.com/~data",
      "Flipboard":"https://flipboard.com/@data",
      "Codecademy":"https://www.codecademy.com/data",
      "Roblox":"http://www.roblox.com/user.aspx?username=data",
      "Gravatar":"https://en.gravatar.com/data",
      "Trip":"https://www.trip.skyscanner.com/user/data",
      "Pastebin":"https://pastebin.com/u/data",
      "BlipFM":"https://blip.fm/data",
      "StreamMe":"https://www.stream.me/data",
      "IFTTT":"https://ifttt.com/p/data",
      "CodeMentor":"https://www.codementor.io/data",
      "Soupio":"http://data.soup.io/",
      "Fiverr":"https://www.fiverr.com/data",
      "Trakt":"https://trakt.tv/users/data",
      "Hackernews":"https://news.ycombinator.com/user?id=data",
      "five00px":"https://500px.com/data",
      "Spotify":"https://open.spotify.com/user/data",
      "Houzz":"https://www.houzz.es/pro/data/artverlin?irs=US",
      "BuzzFeed":"https://www.buzzfeed.com/data",
      "TripAdvisor":"https://www.tripadvisor.com/members/data",
      "HubPages":"https://hubpages.com/@data",
      "Scribd":"https://www.scribd.com/data",
      "Venmo":"https://venmo.com/data",
      "Strava":"https://strava.com/",
      "Canva":"https://www.canva.com/data",
      "CreativeMarket":"https://creativemarket.com/data",
      "Bandcamp":"https://bandcamp.com/data",
      "ReverbNation":"https://www.reverbnation.com/data",
      "Designspiration":"https://www.designspiration.net/data/",
      "ColourLovers":"http://www.colourlovers.com/lover/data",
      "KanoWorld":"https://world.kano.me/profile/data",
      "Badoo":"https://badoo.com/en/profile/data",
      "Newgrounds":"https://data.newgrounds.com/",
      "Patreon":"https://www.patreon.com/data",
      "Mixcloud":"https://www.mixcloud.com/data/",
      "Gumroad":"https://gumroad.com/data",
      "Quora":"https://data.quora.com/",
      "Rankia":"https://www.rankia.com/usuarios/data",
      "El Mundo":"http://www.elmundo.es/social/usuarios/data",
      "Twicsy":"https://twicsy.com/u/data",
      "Gapyear":"http://es.gravatar.com/data.json",
      "Tradimo":"http://en.tradimo.com/profile/data",
      "Eyeem":"https://www.eyeem.com/u/data",
      "QQ":"http://bbs.map.qq.com/space-username-data.html",
      "Verbling":"https://www.verbling.com/profesores/data",
      "Pastebin":"http://pastebin.com/u/data",
      "Meneame":"https://meneame.net/user/"}

def clean_webs(response, name):
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    
    if name == "Ebay": 
        if "The User ID you entered was not found" in soup.text:
            return False
    elif name == "Hackernews":
        if "No such user" in soup.text:
            return False
    elif name == "Mixcloud":
        if "Page Not Found" == soup.text[0:15].strip():
            return False
    elif name == "Twitch":
        if "Lo sentimos" in soup.text:
            return False
    elif name == "Steam":
        if "The specified profile could not be found" in soup.text:
            return False
    elif name == "KanoWorld":
        if "Page could not be found" in soup.text:
            return False
    return True

def getnickWebs(nick):
    dictWebs=dict()
    for name,url in urls.items():
        try:
            url=url.replace("data",nick)
            response=requests.get(url, allow_redirects=False)
            if str(response)[11]!="4" and str(response)[11]=="2":
                if name == "Pastebin" and response.url != "https://pastebin.com/index":
                    dictWebs[name]=response.url
                elif name == "Yelp" and response.url != "https://www.yelp.com/":
                    dictWebs[name]=response.url
                elif name == "GoodReads":
                    dictWebs[name]=response.url
                elif name == "Roblox":
                    dictWebs[name]=response.url
                elif url.lower() == str(response.url).lower():
                    val=clean_webs(response, name)
                    if val:
                        dictWebs[name]=response.url
                else:
                    pass
        except requests.exceptions.ConnectionError:
            continue
    return dictWebs

#Funcion para buscar en Google
def search_google_(target):
    global rep

    engine = Google()
    results = engine.search("'" + target + "'")
    for r in results:

        title = r["title"]
        link = r["text"]
        text = r["text"]

        print("|")
        print ("|----[INFO][GOOGLE][RESULTS][>] " + r["title"])
        print ("|----[INFO][GOOGLE][RESULTS][DESCRIPTION][>] " + r["text"])
        print ("|----[INFO][GOOGLE][RESULTS][LINK][>] " + r["link"])
        
        try:
            tsd, td, tsu = extract(r["link"])
            domain = td + '.' + tsu

            spain_newspaper = open("data/newspaper/spain-newspaper.txt", "r")

            for news in spain_newspaper:

                if domain == news.strip():

                    newspaper.news_parser(r["link"], target)
                    rep.add_markdown(f"[PRENSA]")
                    rep.add_markdown(f"- Título: {title} | Enlace: {link} | Descripción: {text}")

                if domain in config.BL_parserPhone:

                    rep.add_markdown(f"[REDES SOCIALES]")
                    rep.add_markdown(f"- Título: {title} | Enlace: {link} | Descripción: {text}")

                if not domain in config.BL_parserPhone:
                    rep.add_markdown(f"[OTROS]")
                    rep.add_markdown(f"- Título: {title} | Enlace: {link} | Descripción: {text}")
        
            print("|")

        except Exception as e:
            print ("|----[ERROR][HTTP CONNECTION][>] " + str(e))

def main():
    #Imprimimos el banner
    print(config.banner)

    nick = input("Insert nick:")

    #Creamos el report
    now = datetime.now()

    rep.add_title(f"INFORME {now}")
    rep.add_title("BUSCADOR DE NICK", level=2)
    rep.add_markdown("![alt text](images/DG-minimal-version.png 'Logo DG')")
    rep.add_markdown("=====================================================")
    rep.add_markdown(f"- Target: {nick}")
    rep.add_markdown("=====================================================")

    #Buscamos en facebook
    m = input("|----[Q][>] Do you want to find a post on Facebook where this nick apperars? Select Yes[Y]/No[n]: ")
    if m == "y" or m == "Y":
            
        facebook.get_postsFB(nick)
        print("|y")
    else:

        print("|")

    #Buscamos emails
    m = input("|----[Q][>] Do you want to search for emails with that NICK in different providers? Select Yes[Y]/No[n]: ")

    if m == "y" or m == "Y":

        rep.add_title("[EMAILS ENCONTRADOS]", level = 3)
        for email in emails:
            target = nick + email
            try:
                is_valid = validate_email(target, check_regex=True, check_mx=True, smtp_timeout=10, dns_timeout=10, use_blacklist=True)
                if is_valid:
                    print("|----[INFO][EMAIL][>] " + target)
                    print("|--------[INFO][EMAIL][>] Email validated...")
                    rep.add_markdown(f"- {target}")
                    
                else:

                    print("|----[INFO][TARGET][>] " + target)
                    print("|--------[INFO][EMAIL][>] It's not created...")

            except Exception as e:
                
                print(e)
                print("[INFO][TARGET][>] " + target)
                print("|--[INFO][EMAIL] No verification possible... ")
        print("|")
    else:
        print("|")


    #Buscamos en las plataformas
    m = input("|----[Q][>]Do yoy want to search more than 100 platforms if thre is a user with that nickname? Select Yes[Y]/No[n]: ")

    if m == "y" or m == "Y":

        #Creamos título en el report
        rep.add_title("[CUENTAS ENCONTRADAS]", level = 3)

        print("\n This process may take a few minutes...")
        r_nicks = getnickWebs(nick)

        for n in r_nicks:

            NICK = r_nicks.get(n).replace("data", nick)
            print("|----[INFO][" + n.upper() + "][>] " + NICK)
            rep.add_markdown(f"- {NICK}")
    else:
        print("|")
    
    #Buscamos en Google

    m = input("|----[Q][>] Do you want to Google the nickname and classify the results? Select Yes[Y]/No[n]: ")

    if m == "y" or m == "Y":

        rep.add_title("[Google Hacking & Clustering]", level = 3)
        search_google_(nick)
    else:
        print("|")

    #IMPRIMIMOS EL INFORME
    print("|----[INFO][REPORT][>] You can now see your PDF report (report.html)...")
    rep.write_report()

if __name__ == "__main__":
    main()