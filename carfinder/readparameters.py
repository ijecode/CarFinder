import yaml
import datetime

class params:
    searchCriteria = {}
    sites = {}
    notifications = {}
    acceptableTransmissionValues = ['automatic','manual','any']

    def __init__(self) -> None:
        try:
            stream = open('parameters.yaml', 'r')
            yamlFile = yaml.load(stream, yaml.CLoader)
        except Exception as e:
            print(e)
            print('Issues loading parameters.yaml, exiting...')
            exit()

        params.searchCriteria = yamlFile['searchCriteria']
        params.sites = yamlFile['sites']
        params.notifications = yamlFile['notifications']

        self.qualityCheckAndCleanUp()
        self.scanForMissingParameters()
        if 'gumtree' in params.sites and params.sites['gumtree'] == True:
            print('gumree found, calculating...')
            self.gumtreeYearCalculation()

    def scanForMissingParameters(self):
        requiredSearchCriteriaParameters = ['postcode']
        try:
            for requiredSearchCriteria in requiredSearchCriteriaParameters:
                if requiredSearchCriteria not in params.searchCriteria:
                    raise Exception('Required Search Criteria %s is not present' %requiredSearchCriteria)
            if True not in params.sites.values():
                raise Exception('At least one site must be enabled for searching')
            if params.notifications['pushover']['enabled'] == True:
                if 'userKey' or 'apiKey' not in params.notifications['pushover'].values():
                    raise Exception('Missing required userKey/apiKey for Pushover notifications')
                if params.notifications['pushover']['userKey'] or params.notifications['pushover']['apiKey'] == 'your_key_here':
                    raise Exception('To enable Pushover notifications, set your user key and api key')
        except Exception as e:
            print(e)
            print('Issues with YAML parameter file detected, exiting...')
            exit()

    def qualityCheckAndCleanUp(self):   
        integerParameters = ['distance', 'priceMin', 'priceMax', 'mileage', 'yearMin', 'yearMax'] 
        minMaxPairs = [['priceMin', 'priceMax'],['yearMin', 'yearMax']]
        for pair in minMaxPairs:
            self.minMaxCheck(params.searchCriteria[pair[0]], params.searchCriteria[pair[1]])
        for key, value in params.searchCriteria.items():
            try:
                # General checks
                if value is None:
                    raise Exception('Parameter %s is empty' %value)
                # Check values
                if key in integerParameters:
                    self.integerQualityCheck(key, value)
                elif key == 'postcode':
                    print('found postcode')
                    if len(value) < 6:
                        raise Exception('Postcode %s is less than 6 characters' %value)
                    if len(value) > 8:
                        raise Exception('Postcode %s is greater than 8 characters' %value)
                    # Strip any whitespace
                    params.searchCriteria[key] = value.replace(' ', '')
                elif key == 'transmission':
                    self.transmissionCheck(value)
            except Exception as e:
                self.yamlThrow(e)

    def integerQualityCheck(self, key, value):
        try:
            if type(value) is not int:
                raise Exception('%s %s is not an integer' %(key, value))
            elif value < 0:
                raise Exception('%s %s value must be positive or 0' %(key, value))
        except Exception as e:
            self.yamlThrow(e)

    def minMaxCheck(self, min, max):
        if(max != 0 and min > max):
            self.yamlThrow(Exception('Minimum value %s is greater than maximum value %s' %(min, max)))
    
    def transmissionCheck(self, value):
        if value not in self.acceptableTransmissionValues:
            raise Exception('Transmission value %s is not in the accepted list of transmission values: %s' %(value, self.acceptableTransmissionValues))

    # Gumtree doesn't allow searching by year range, instead essentially asking how old should the car be. 
    # Attempt to translate yearMin value into this age criteria
    def gumtreeYearCalculation(self):
        if 'yearMin' in self.searchCriteria and self.searchCriteria['yearMin'] > 0:
            now = datetime.datetime.now().year
            difference = now - self.searchCriteria['yearMin']
            if difference > 10:
                self.searchCriteria.update({'gumtreeYear': 'over_10'})
            else:
                queryString = 'up_to_%s' %difference
                self.searchCriteria.update({'gumtreeYear': queryString})
        print('gumtreeYear value added')
        print(params.searchCriteria['gumtreeYear'])

    def yamlThrow(self, exception):
        print(exception)
        print('Issues with YAML parameter file detected, exiting...')
        exit()
