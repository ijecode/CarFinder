import sqlitedict
import readparameters
import urlConstructor
import scraper
import notifications

#TODO:
# - database handling - first run
# - separate tables per site?
# - notifications class?
# - Handle multiple parameter files

# DB setup
db = sqlitedict.SqliteDict('cars.db')

parameters = readparameters.params()

urls = urlConstructor.urlConstructor(parameters)

newCars = scraper.scrape(urls.urls, db)

notifications.notify(parameters.notifications, newCars, db)

db.close()