class urlConstructor:
    urls = {}

    autoTraderUrlQueryStrings = {'postcode': 'postcode',
                                'distance': 'radius',
                                'transmission': 'transmission',
                                'make': 'make',
                                'model': 'model',
                                'priceMin': 'price-from',
                                'priceMax': 'price-to',
                                'yearMin': 'year-from',
                                'yearMax': 'year-to',
                                'mileage': 'maximum-mileage'}

    gumtreeUrlQueryStrings = {'postcode': 'search_location',
                            'distance': 'radius',
                            'transmission': 'vehicle_transmission',
                            'make': 'vehicle_make',
                            'model': 'vehicle_model',
                            'priceMin': 'min_price',
                            'priceMax': 'max-price',
                            'gumtreeYear': 'vehicle_registration_year',
                            'mileage': 'vehicle_mileage'}

    def __init__(self, params) -> None:
        for k, v in params.sites.items():
            if v == True:
                if k == 'autotrader':
                    self.autoTraderUrlConstruction(params)
                elif k == 'gumtree':
                    self.gumtreeUrlConstruction(params)
                elif k == 'ebay':
                    self.ebayUrlConstruction(params)

    def autoTraderUrlConstruction(self, params):
        urlPieces = []
        urlPieces.append('https://www.autotrader.co.uk/car-search?sort=datedesc')

        for key, value in params.searchCriteria.items():
            if key in self.autoTraderUrlQueryStrings:
                if value != 0 and value != 'any':
                    if key == 'transmission':
                        # Oddly, transmission query needs to be capitalised to work
                        queryString ='&%s=%s' %(self.autoTraderUrlQueryStrings[key], value.capitalize())
                        urlPieces.append(queryString)
                    else:
                        queryString = '&%s=%s' %(self.autoTraderUrlQueryStrings[key], value)
                        urlPieces.append(queryString)

        self.urls.update({'autotrader': ''.join(urlPieces)}) 
    
    def gumtreeUrlConstruction(self, params):
        urlPieces = []
        urlPieces.append('https://www.gumtree.com/search?search_category=cars')

        for key, value in params.searchCriteria.items():
            if key in self.gumtreeUrlQueryStrings:
                if value != 0 or value != 'any':
                    if key == 'mileage':
                        urlPieces.append('&up_to_%s=%s' %(self.gumtreeUrlQueryStrings[key], value))
                    else:
                        urlPieces.append('&%s=%s' %(self.gumtreeUrlQueryStrings[key], value))

        self.urls.update({'gumtree': ''.join(urlPieces)}) 

    def ebayUrlConstruction(self, params):
        urlPieces = []
        urlPieces.append('https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw=car&_sacat=9801&')
        urlPieces.append('&_stpos=%s' % params.searchCriteria['postcode'])

        self.urls.update({'ebay': ''.join(urlPieces)}) 
