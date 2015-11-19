import urllib, urllib2
from dateutil.parser import *
from bs4 import BeautifulSoup, Comment, Doctype, NavigableString

# TODO: Remove need for strange global variable.
source = ''

def crawlContent(jokes):
    """Download and crawl the URLs stored in several jokes."""

    global source

    for joke in jokes:

        if joke.sourceURL:
            try:
                html = urllib2.urlopen(a.url).read()
                source = joke.source

                soup = BeautifulSoup(html, 'html.parser')
                soup = removeHeaderNavFooter(soup, source)
                soup = removeComments(soup, source)
                soup = removeScriptStyle(soup, source)
                soup = removeAds(soup, source)

                content = getContent(soup)

                joke.content = content

                jokes[i] = joke
                with open("test.html", "w") as f:
                    f.write(soup.prettify('utf-8'))
                # with open("test.txt", "w") as f:
                #   f.write(cont)
            except:
                pass
    return jokes

def removeHeaderNavFooter(soup, source):
    hnfs = soup.findAll({'header', 'nav', 'footer', 'aside'})
    [hnf.extract() for hnf in hnfs]
    return soup

def removeScriptStyle(soup, source):
    hnfs = soup.findAll({'style', 'script', 'noscript', '[document]', 'head', 'title', 'form'})
    [hnf.extract() for hnf in hnfs]
    return soup

# TODO: May not want to remove comments for jokes
def removeComments(soup, source):
    comments = soup.findAll(text=lambda text:isinstance(text, Comment) or text.find('if') != -1)
    [comment.extract() for comment in comments]
    return soup

def removeAds(soup, source):
    ads = soup.findAll(adSelect)
    [ad.extract() for ad in ads]
    return soup

def adSelect(tag): # this is the selector for ads, recommended articles, etc
    idList = ['most-popular-parsely', 'specialFeature', # Reuters
    'orb-footer', 'core-navigation', 'services-bar', # BBC
    'profile-cards' #VentureBeat
    ]

    classList = {}

    # TODO: Left cnn and business_insider as examples. Work to be done here

    classList['cnn'] = ['ob_widget', 'zn-staggered__col', 'el__video--standard', 'el__gallery--fullstandardwidth', 'el__gallery-showhide', 'el__gallery', 'el__gallery--standard', 'el__featured-video', 'zn-Rail', 'el__leafmedia']

    classList['business_insider'] = ['abusivetextareaDiv', 'LoginRegister', 'rhsb', 'TabsContList', 'rhs_nl', 'sticky', 'rhs', 'titleMoreLinks', 'ShareBox', 'Commentbox', 'commentsBlock', 'RecommendBlk', 'prvnxtbg', 'OUTBRAIN', 'AuthorBlock', 'seealso', 'Joindiscussion', 'subscribe_outer']

    # TODO: Add the classes used by reddit ads
    classList['reddit'] = []

    global source

    if tag.has_attr('id') and tag.get('id') in idList:
        return True
    if tag.has_attr('class'):
        c = tag.get('class')
        for className in classList[source]:
            if className in c:
                return True
    return False

def getProfile(soup):
    # page = requests.get('https://www.reddit.com/r/Jokes/comments/3tfdo5/pretty_woman_sneezes/')
    # tree = html.fromstring(page.content)
    alldiv = soup.findAll('p', { "class" : "tagline" })
    for div in alldiv:
        print div.a['href']

def getContent(soup):
    elems = soup.findAll(text=True and visible)
    buildText = []
    for elem in elems:
        if isinstance(elem, NavigableString):
            txt = elem.encode('utf-8')
            # score = calcScore(elem, txt)
            # if score > 0:
                # print "[",score,"]", txt
            buildText.append(txt)
        else:
            pass
    return "\n".join(buildText)

def isDate(txt):
    try:
        dt = parse(txt)
        return True
    except:
        return False

def calcScore(el, txt):
    txtLower = txt.lower()
    score = 1 # you have to at least get to 0
    if len(txt) < 5:
        score -= 100
    if len(txt) > 100: # at least some sentence
        score += 50
    if isDate(txt):
        score -= 100
        return score
    if len(txt) <= 25:
        shareKeywords = ['facebook', 'twitter', 'google plus', 'email', 'linkedin', 'google+', 'whatsapp', 'pinterest', 'snapchat', 'share', 'report', 'skip', 'more', 'post', 'comment', 'tweet', 'print']
        for key in shareKeywords:
            if key in txtLower:
                score -= 30
    if len(txt) <= 70:
        if ('created' in txtLower or 'date' in txtLower or 'photograph:' in txtLower or 'browser' in txtLower or 'adobe' in txtLower or 'try again' in txtLower or 'upgrade' in txtLower or 'please install' in txtLower):
            score -= 30
    if ('http://' in txt or '.com' in txt or '.org' in txt or 'www.' in txt) and ' ' not in txt: # what if it's a link
        score -= 30
    if txt in ['Events', 'Terms of Service', 'Home', 'Privacy Policy', 'VentureBeat', 'Mobile', 'Guest', 'About', 'Topics', 'More news', 'See Also', 'close']:
        score -= 100
    return score

def visible(element):
    """Return true if the element is probably visible on page if you scrolled around."""
    if element.parent.name in ['style', 'script', 'noscript', '[document]', 'head', 'title']:
        return False
    return True
