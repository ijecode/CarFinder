from bs4 import BeautifulSoup
import urllib.request

def scrape(urls, db):
    newCars = []

    if 'autotrader' in urls:
        newCars += scrapeAutoTrader(urls['autotrader'], db)
    if 'gumtree' in urls:
        newCars += scrapeGumTree(urls['gumtree'], db)

    return newCars

def scrapeGumTree(url, db):
    print('scraping gumtree')
    newCars = []

    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        cars = soup.find_all('article', class_='listing-maxi')

        if len(cars) == 0:
            raise Exception('No cars found on Gumtree - check your search criteria and expand if necessary')

        for car in cars:
            if car.has_attr('data-q'):
                id = int(car.attrs.get('data-q')[3:])

                if(id not in db):
                    make = car.find(class_='listing-title').text.strip()
                    details = car.find(class_="listing-description").text.strip()[:20] + '...'
                    price = car.find(class_='listing-price').text.strip()
                    url = "https://www.gumtree.co.uk" + car.find('a', class_='listing-link').attrs.get('href')
                    db[id] = {'site': 'gumtree', "make": make,"details": details,"price": price,"url": url}
                    db.commit()
                    newCars.append(id)

    except Exception as e:
        print(e)
        exit()
    
    return newCars

def scrapeAutoTrader(url, db):
    newCars = []

    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')

        cars = soup.find_all(class_='search-page__result')

        if len(cars) == 0:
            raise Exception('No cars found on Autotrader - check your search criteria and expand if necessary')

        for car in cars:
            id = int(car['id'])

            # See if car already exists in the db
            if(id not in db):
                make = car.find(class_='product-card-details__title').text.strip()
                details = car.find(class_='product-card-details__subtitle').text.strip()
                price = car.find(class_='product-card-pricing__price').text.strip()
                url = 'https://www.auto-trader.co.uk' + car.find('a', attrs={'data-label': 'search appearance click '}).attrs.get('href')
                db[id] = {'site': 'autotrader', 'make': make,'details': details,'price': price,'url': url}
                db.commit()
                newCars.append(id)
        
    except Exception as e:
        print(e)
        exit()
    
    return newCars

