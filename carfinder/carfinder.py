import sqlitedict
import http.client
import readparameters
import urlConstructor
import scraper
import urllib

#TODO:
# - database handling - first run
# - separate tables per site?
# - notifications class?
# - Handle multiple parameter files

# DB setup
db = sqlitedict.SqliteDict('autotrader.db')

parameters = readparameters.params()
urls = urlConstructor.urlConstructor(parameters)
newCars = scraper.scrape(urls.urls, db)

for car in newCars:
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": parameters.notifications['pushover']['apiKey'],
        "user": parameters.notifications['pushover']['userKey'],
        "message": "New Car Located on %(site)s: %(make)s, %(price)s" % db[car],
        "url" : "%(url)s" % db[car]
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

db.close()