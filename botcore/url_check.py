from pysafebrowsing import SafeBrowsing
import urllib
import bs4
import re
import os

safeweb_api_key = os.environ.get('safeweb_api_key')
def check_url_google(url):
    s = SafeBrowsing(safeweb_api_key)
    result = s.lookup_urls([url])
    return result[url]['malicious']

def check_url(url):
    target=urllib.parse.quote_plus(url)
    url = f'https://safeweb.norton.com/report/show?url={target}'
    html = urllib.request.urlopen(url)
    bsoup = bs4.BeautifulSoup(html.read(), 'html.parser')
    return bsoup.find('b').text.lower()

def search_url(text):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,text)
    result=[x[0] for x in url]
    if len(result) > 0:
        return result
    else:
        return None