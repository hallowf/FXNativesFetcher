# FXNativesFetcher

## What it does

* Goes to https://runtime.fivem.net/doc/natives
* Parses the html and appends found natives to a list removing everything between "()"
* Scrolls down and repeats the above step until it can't find more natives
* Makes all functions "pretty" and returns a string with all of them so you can add it to your luacheck or make a linter or something like that...

## REQUIREMENTS

* [Python3](https://www.python.org/download/releases/3.0/)

* [chromedriver](http://chromedriver.chromium.org/), download it and put it inside the "bin" *lowercase* folder if it doesn't exist create one

This also requires and the following packages to be installed
* Selenium
* BeautifulSoup4

```
pip install -r requirements.txt
```

## DISCLAIMER

All trademarks and registered trademarks are the property of their respective owners.

This software is not affiliated with CitizenFX
Collective (“CitizenFX”), any parent, or affiliate corporation. All products and brands mentioned are the respective trademarks and copyrights of their owners. All material found here is intended for research purposes only.

## Notes

1. The website is built with a js framework so this won't work as is
```
from html.parser import HTMLParser
import urllib.request as request

url_to_parse = "https://runtime.fivem.net/doc/natives/"


class Parser(HTMLParser):
    # Initializing lists
    lsStartTags = list()
    lsEndTags = list()
    lsStartEndTags = list()
    lsComments = list()

    # HTML Parser Methods
    def handle_starttag(self, startTag, attrs):
        self.lsStartTags.append(startTag)

    def handle_endtag(self, endTag):
        self.lsEndTags.append(endTag)

    def handle_startendtag(self, startendTag, attrs):
        self.lsStartEndTags.append(startendTag)

    def handle_comment(self, data):
        self.lsComments.append(data)


# Create object of overriden class
parser = Parser()

# create request with costum user-agent
req = request.Request(url_to_parse, headers={'User-Agent': 'Mozilla/5.0'})

# Open webpage
html = request.urlopen(req)

# Feed to parser
parser.feed(str(html.read))

# printing the extracted values
print("Start tags", parser.lsStartTags)
print("End tags", parser.lsEndTags)
print("Start End tags", parser.lsStartEndTags)
print("Comments", parser.lsComments)

```

2. All elements are stored in one list but the maximum size of a python list on a 32 bit system is around 500,000,000 elements so it shouldn't be a problem

3. Selenium works great altough it seems to crash using chromedriver maybe because of my system's high ram usage or having another chrome window playing music on youtube with **several** tabs open **DIDN'T TEST FIREFOX**

4. [HTMLParser](https://docs.python.org/3/library/html.parser.html) might be possible to use but selenium seems to be easier

5. [CasperJS](http://casperjs.org/) might also work haven't tried it
