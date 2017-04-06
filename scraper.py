# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

import scraperwiki
from bs4 import BeautifulSoup
import json

# import lxml.html
#
# # Read in a page
result = {}
html = scraperwiki.scrape("http://www.gat.no/nyheter/tok-ni-for-fart-og-en-for-mobilbruk-1.1802906")
bs = BeautifulSoup(html, "html5lib")
article = bs.find("article", {"class": "full_article"})

result["index"] = "1"
header = article.find("header")
result["overskrift"] = header.find("h1").text.strip()
overskrift = result["overskrift"]
result["ingress"] = header.find("h2", {"class": "light"}).text.strip()
result["publiseringsdato"] = header.find("time", {"class": "op-published"})["datetime"]
result["oppdateringsdato"] = header.find("time", {"class": "op-modified"})["datetime"]
result["forfatter"] = header.find("ul", {"class": "author_details"}).text.strip()

header.extract()
body = ""
for p in article("p"):
    if p:
        if p.text:
            body += p.text.strip() + " "
        elif p.string:
            body += p.string.strip() + " "

if len(body.strip()) > 0:
    result["body"] = body
print(json.dumps(result, indent=1))
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
#scraperwiki.sqlite.create_table(unique_keys=["overskrift"])
scraperwiki.sqlite.save(unique_keys=["index"], data=result, table_name="data")

#
# # An arbitrary query against the database
herro = scraperwiki.sql.select("* from data")
print(herro)

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".
