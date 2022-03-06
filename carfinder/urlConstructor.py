class urlConstructor:
    urls = {}

    def __init__(self, params) -> None:
        for k, v in params.sites.items():
            if v == True:
                if k == 'autotrader':
                    self.autoTraderUrlConstruction(params)
                elif k == 'gumtree':
                    self.gumtreeUrlConstruction(params)

    def autoTraderUrlConstruction(self, params):
        urlPieces = []
        urlPieces.append('https://www.autotrader.co.uk/car-search?sort=datedesc')
        urlPieces.append('&postcode=%s' % params.searchCriteria['postcode'])

        if 'distance' in params.searchCriteria and params.searchCriteria['distance'] != 'max':
            urlPieces.append('&radius=%s' % str(params.searchCriteria['distance']))
        if 'priceMax' in params.searchCriteria and params.searchCriteria['priceMax'] != 'any':
            urlPieces.append('&price-to=%s' % params.searchCriteria['priceMax'])
        if 'transmission' in params.searchCriteria and params.searchCriteria['transmission'] != 'any':
            urlPieces.append('&transmission=%s' % params.searchCriteria['transmission'].capitalize())

        self.urls.update({'autotrader': ''.join(urlPieces)}) 
    
    def gumtreeUrlConstruction(self, params):
        urlPieces = []
        urlPieces.append('https://www.gumtree.com/search?search_category=cars')
        urlPieces.append('&search_location=%s' % params.searchCriteria['postcode'])
        if 'distance' in params.searchCriteria and params.searchCriteria['distance'] != 'max':
            urlPieces.append('&distance=%s' % str(params.searchCriteria['distance']))
        if 'priceMax' in params.searchCriteria and params.searchCriteria['priceMax'] != 'any':
            urlPieces.append('&max_price=%s' % params.searchCriteria['priceMax'])
        if 'transmission' in params.searchCriteria and params.searchCriteria['transmission'] != 'any':
            urlPieces.append('&vehicle_transmission=%s' % params.searchCriteria['transmission'])
        
        self.urls.update({'gumtree': ''.join(urlPieces)}) 

